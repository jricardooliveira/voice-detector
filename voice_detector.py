#!/usr/bin/env python3
import argparse
import json
import math
import os
import subprocess
import sys
import wave
import webrtcvad
import glob

# ---------- Helpers ----------
def ffprobe_channels(path):
    """Return number of audio channels using ffprobe."""
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=channels",
            "-of", "default=nk=1:nw=1",
            path
        ], text=True).strip()
        return int(out)
    except Exception:
        return 1  # fallback

def ffmpeg_to_pcm_mono(path, channel=None, sample_rate=16000):
    """
    Use ffmpeg to produce 16-bit PCM mono (little endian) for a specific channel.
    If channel is None and the source is mono, just decode mono.
    If channel in {0,1}, map left/right from a stereo source.
    Returns (pcm_bytes, sample_rate).
    """
    args = ["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-acodec", "pcm_s16le", "-ar", str(sample_rate)]
    if channel is None:
        args += ["-ac", "1"]
    else:
        # map specific channel to mono: 0 = left, 1 = right
        # amerge not needed; use pan filter
        pan_map = f"pan=mono|c0=c{channel}"
        args = ["ffmpeg", "-v", "error", "-i", path, "-af", pan_map, "-f", "s16le", "-acodec", "pcm_s16le", "-ar", str(sample_rate)]
    args += ["-"]
    try:
        pcm = subprocess.check_output(args)
        return pcm, sample_rate
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}", file=sys.stderr)
        sys.exit(3)

def frame_generator(pcm_bytes, sample_rate, frame_ms):
    """Yield successive frames (bytes) of length frame_ms at 16-bit mono."""
    bytes_per_sample = 2
    frame_bytes = int(sample_rate * (frame_ms / 1000.0) * bytes_per_sample)
    for i in range(0, len(pcm_bytes) - frame_bytes + 1, frame_bytes):
        yield pcm_bytes[i:i + frame_bytes]

def voiced_ratio(pcm_bytes, sample_rate, frame_ms=30, vad_mode=2):
    """
    Return fraction of frames classified as speech by webrtcvad.
    vad_mode: 0=menos agressivo, 3=mais agressivo (mais fácil dar falso negativo).
    """
    vad = webrtcvad.Vad(vad_mode)
    total = 0
    voiced = 0
    for f in frame_generator(pcm_bytes, sample_rate, frame_ms):
        total += 1
        if vad.is_speech(f, sample_rate):
            voiced += 1
    return (voiced / total) if total else 0.0

def process_audio_file(file_path, threshold, frame_ms, vad_mode):
    """Process a single audio file and return results."""
    try:
        channels = ffprobe_channels(file_path)
        results = []

        if channels >= 2:
            # Leg A: canal esquerdo (0) — operador (por convenção)
            pcmA, sr = ffmpeg_to_pcm_mono(file_path, channel=0, sample_rate=16000)
            rA = voiced_ratio(pcmA, sr, frame_ms=frame_ms, vad_mode=vad_mode)
            results.append({"leg": "A", "channel": 0, "voiced_ratio": rA})

            # Leg B: canal direito (1) — cliente
            pcmB, sr = ffmpeg_to_pcm_mono(file_path, channel=1, sample_rate=16000)
            rB = voiced_ratio(pcmB, sr, frame_ms=frame_ms, vad_mode=vad_mode)
            results.append({"leg": "B", "channel": 1, "voiced_ratio": rB})
        else:
            # Mono: analisar uma única faixa (separação em legs não é possível aqui)
            pcm, sr = ffmpeg_to_pcm_mono(file_path, channel=None, sample_rate=16000)
            r = voiced_ratio(pcm, sr, frame_ms=frame_ms, vad_mode=vad_mode)
            results.append({"leg": "mono", "channel": 0, "voiced_ratio": r})

        # Check for silent legs
        bad_legs = [x for x in results if x["voiced_ratio"] < threshold]
        
        return {
            "file": file_path,
            "channels_detected": channels,
            "legs": results,
            "has_voice": len(bad_legs) == 0,
            "silent_legs": [x["leg"] for x in bad_legs],
            "max_voiced_ratio": max([x["voiced_ratio"] for x in results]) if results else 0.0
        }
    except Exception as e:
        return {
            "file": file_path,
            "error": str(e),
            "has_voice": False,
            "silent_legs": ["error"]
        }

def process_folder(folder_path, threshold, frame_ms, vad_mode, json_output=False):
    """Process all audio files in a folder."""
    # Supported audio extensions
    audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.aac', '*.flac', '*.ogg']
    
    # Find all audio files
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(folder_path, ext)))
        audio_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not audio_files:
        print(f"No audio files found in {folder_path}")
        return
    
    print(f"Found {len(audio_files)} audio files in {folder_path}")
    print("=" * 60)
    
    all_results = []
    silent_files = []
    
    for i, file_path in enumerate(audio_files, 1):
        filename = os.path.basename(file_path)
        print(f"[{i}/{len(audio_files)}] Processing: {filename}")
        
        result = process_audio_file(file_path, threshold, frame_ms, vad_mode)
        all_results.append(result)
        
        if not result.get("has_voice", False):
            silent_files.append(result)
            print(f"  ❌ NO VOICE DETECTED")
        else:
            max_ratio = result.get("max_voiced_ratio", 0)
            print(f"  ✅ Voice detected: {max_ratio:.1%} max activity")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Total files processed: {len(audio_files)}")
    print(f"Files with voice: {len(audio_files) - len(silent_files)}")
    print(f"Files without voice: {len(silent_files)}")
    
    if silent_files:
        print(f"\n🚨 FILES WITHOUT VOICE:")
        for result in silent_files:
            filename = os.path.basename(result["file"])
            if "error" in result:
                print(f"  - {filename} (ERROR: {result['error']})")
            else:
                silent_legs = ", ".join(result["silent_legs"])
                print(f"  - {filename} (silent legs: {silent_legs})")
    else:
        print("\n✅ All files have voice activity!")
    
    if json_output:
        output = {
            "folder": folder_path,
            "threshold": threshold,
            "frame_ms": frame_ms,
            "vad_mode": vad_mode,
            "total_files": len(audio_files),
            "files_with_voice": len(audio_files) - len(silent_files),
            "files_without_voice": len(silent_files),
            "results": all_results,
            "silent_files": [{"file": r["file"], "silent_legs": r.get("silent_legs", [])} for r in silent_files]
        }
        print(f"\nJSON Output:")
        print(json.dumps(output, indent=2))
    
    return len(silent_files) > 0

# ---------- Main ----------
def main():
    parser = argparse.ArgumentParser(
        description="Voice activity detection tool for analyzing audio recordings using Google's WebRTC VAD."
    )
    parser.add_argument("input", help="Audio file or folder with audio files (WAV/MP3/M4A/AAC/FLAC/OGG with 1 or 2 channels).")
    parser.add_argument("--threshold", type=float, default=0.10,
                        help="Minimum voice activity ratio per leg (default: 0.10 = 10 percent).")
    parser.add_argument("--frame-ms", type=int, default=30,
                        help="Frame duration in ms (10/20/30, default: 30).")
    parser.add_argument("--vad-mode", type=int, default=2, choices=[0,1,2,3],
                        help="VAD aggressiveness (0 least aggressive, 3 most aggressive).")
    parser.add_argument("--json", action="store_true", help="Output in JSON format.")
    args = parser.parse_args()

    # Check if input is a file or folder
    if os.path.isdir(args.input):
        # Process folder
        has_silent_files = process_folder(args.input, args.threshold, args.frame_ms, args.vad_mode, args.json)
        sys.exit(2 if has_silent_files else 0)
    else:
        # Process single file (original functionality)
        channels = ffprobe_channels(args.input)
        results = []

        if channels >= 2:
            # Leg A: canal esquerdo (0) — operador (por convenção)
            pcmA, sr = ffmpeg_to_pcm_mono(args.input, channel=0, sample_rate=16000)
            rA = voiced_ratio(pcmA, sr, frame_ms=args.frame_ms, vad_mode=args.vad_mode)
            results.append({"leg": "A", "channel": 0, "voiced_ratio": rA})

            # Leg B: canal direito (1) — cliente
            pcmB, sr = ffmpeg_to_pcm_mono(args.input, channel=1, sample_rate=16000)
            rB = voiced_ratio(pcmB, sr, frame_ms=args.frame_ms, vad_mode=args.vad_mode)
            results.append({"leg": "B", "channel": 1, "voiced_ratio": rB})
        else:
            # Mono: analisar uma única faixa (separação em legs não é possível aqui)
            pcm, sr = ffmpeg_to_pcm_mono(args.input, channel=None, sample_rate=16000)
            r = voiced_ratio(pcm, sr, frame_ms=args.frame_ms, vad_mode=args.vad_mode)
            results.append({"leg": "mono", "channel": 0, "voiced_ratio": r})

        # Avaliação e saída
        bad_legs = [x for x in results if x["voiced_ratio"] < args.threshold]

        if args.json:
            out = {
                "file": args.input,
                "threshold": args.threshold,
                "frame_ms": args.frame_ms,
                "vad_mode": args.vad_mode,
                "channels_detected": channels,
                "legs": results,
                "status": "ALERT" if bad_legs else "OK",
                "silent_legs": [x["leg"] for x in bad_legs]
            }
            print(json.dumps(out, indent=2))
        else:
            print(f"Ficheiro: {args.input} | Canais: {channels}")
            for x in results:
                pct = round(100.0 * x["voiced_ratio"], 1)
                print(f"  Leg {x['leg']} (canal {x['channel']}): {pct}% frames com voz")
            if bad_legs:
                legs_str = ", ".join([x["leg"] for x in bad_legs])
                print(f"ALERTA: Voz insuficiente nas legs: {legs_str} (threshold={int(args.threshold*100)}%)")
            else:
                print("OK: Atividade de voz presente em todas as legs.")

        # Código de saída para fácil integração CI/monitorização:
        # 0 = OK; 2 = alerta (voz insuficiente em pelo menos uma perna); 3 = erro processamento
        sys.exit(0 if not bad_legs else 2)

if __name__ == "__main__":
    main()



