import os
import requests
from flask import Flask, request, render_template_string, jsonify

# CREATED BY AZXXKK - FOZ GPT ULTRA V4
# ENHANCEMENT: PHOTO SLIDESHOW SUPPORT + FORCE DOWNLOAD HEADERS

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FOZ GPT - TikTok Downloader ULTRA V4.2</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        body { background-color: #020202; color: #d1d1d1; font-family: 'JetBrains+Mono', monospace; }
        .ui-card { background: #080808; border: 1px solid #1a1a1a; box-shadow: 0 0 30px rgba(0,0,0,0.5); }
        .input-field { background: #000; border: 1px solid #222; color: #00ff41; transition: all 0.2s ease; }
        .input-field:focus { border-color: #00ff41; outline: none; box-shadow: 0 0 8px rgba(0,255,65,0.3); }
        .btn-foz { background: #d1d1d1; color: #000; font-weight: bold; transition: all 0.3s; }
        .btn-foz:hover { background: #00ff41; transform: translateY(-1px); }
        .btn-download { border: 1px solid #333; text-align: center; padding: 10px; font-size: 10px; font-weight: bold; transition: 0.2s; display: block; width: 100%; margin-bottom: 5px; }
        .btn-download:hover { background: #fff; color: #000; border-color: #fff; }
        .loading-pulse { animation: pulse 1.5s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .3; } }
        .img-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 10px; }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-6">
    <div class="max-w-lg w-full p-8 ui-card">
        <div class="mb-8">
            <h1 class="text-2xl font-bold tracking-widest text-white uppercase mb-1">TikTok Engine <span class="text-green-500">[V4.2]</span></h1>
            <p class="text-[10px] text-zinc-600 uppercase tracking-[0.3em]">Engineered by FOZ GPT // azxxkk</p>
        </div>

        <div class="space-y-5">
            <div>
                <label class="text-[10px] uppercase text-zinc-500 mb-2 block tracking-widest">Target URL</label>
                <input type="text" id="tiktokUrl" placeholder="https://vt.tiktok.com/..." class="w-full p-4 input-field text-sm">
            </div>
            <button onclick="executeExtraction()" id="btnAction" class="w-full p-4 btn-foz text-xs uppercase tracking-widest">Extract Media</button>
        </div>

        <div id="loading" class="hidden mt-6 text-center">
            <span class="loading-pulse text-[10px] text-green-500 tracking-tighter italic">PENETRATING TIKTOK DATABASE...</span>
        </div>

        <div id="result" class="hidden mt-8 pt-8 border-t border-zinc-900 space-y-6">
            <div id="mediaPreview" class="relative bg-black border border-zinc-800 overflow-hidden"></div>
            
            <div id="downloadButtons" class="space-y-2">
                <!-- Action Buttons Injected Here -->
            </div>
            
            <button onclick="resetUI()" class="w-full mt-4 text-[9px] text-zinc-700 uppercase hover:text-zinc-400 transition-colors">Clear Session</button>
        </div>

        <div class="mt-12 text-[9px] text-zinc-800 text-center uppercase tracking-[0.5em]">Precision . Logic . Power</div>
    </div>

    <script>
        async function executeExtraction() {
            const url = document.getElementById('tiktokUrl').value;
            const btn = document.getElementById('btnAction');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const preview = document.getElementById('mediaPreview');
            const dlButtons = document.getElementById('downloadButtons');

            if (!url) return;

            btn.disabled = true;
            loading.classList.remove('hidden');
            result.classList.add('hidden');
            dlButtons.innerHTML = '';
            preview.innerHTML = '';

            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                
                const data = await response.json();

                if (data.status === 'success') {
                    if (data.type === 'photo') {
                        // Render Photos
                        let imgHtml = '<div class="img-grid p-4">';
                        data.images.forEach((img, index) => {
                            imgHtml += `<img src="${img}" class="w-full h-auto border border-zinc-800">`;
                            dlButtons.innerHTML += `<a href="${img}" download="photo_${index}.jpg" target="_blank" class="btn-download text-green-400 border-green-900">DOWNLOAD PHOTO ${index + 1}</a>`;
                        });
                        imgHtml += '</div>';
                        preview.innerHTML = imgHtml;
                    } else {
                        // Render Video
                        preview.innerHTML = `<video class="w-full h-full object-contain" controls autoplay muted><source src="${data.sd}" type="video/mp4"></video>`;
                        dlButtons.innerHTML = `
                            <a href="${data.hd}" download="video_hd.mp4" target="_blank" class="btn-download text-green-500 border-green-900">DOWNLOAD VIDEO [HD]</a>
                            <a href="${data.sd}" download="video_sd.mp4" target="_blank" class="btn-download text-blue-500 border-blue-900">DOWNLOAD VIDEO [SD]</a>
                        `;
                    }
                    
                    // Always add Audio
                    dlButtons.innerHTML += `<a href="${data.audio}" download="audio.mp3" target="_blank" class="btn-download text-yellow-500 border-yellow-900">DOWNLOAD AUDIO [MP3]</a>`;
                    
                    result.classList.remove('hidden');
                } else {
                    alert('FAILURE: ' + data.message);
                }
            } catch (err) {
                alert('SYSTEM ERROR: BYPASS FAILED');
            } finally {
                btn.disabled = false;
                loading.classList.add('hidden');
            }
        }

        function resetUI() {
            document.getElementById('tiktokUrl').value = '';
            document.getElementById('result').classList.add('hidden');
            document.getElementById('mediaPreview').innerHTML = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/download', methods=['POST'])
def tiktok_api():
    payload = request.get_json()
    url = payload.get('url')

    if not url:
        return jsonify({"status": "error", "message": "Null Input"}), 400

    try:
        api_url = "https://www.tikwm.com/api/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        data = {'url': url, 'hd': 1}
        
        response = requests.post(api_url, data=data, headers=headers).json()

        if response.get('code') == 0:
            res_data = response['data']
            
            # Check for Photos (Slideshow)
            images = res_data.get('images')
            audio_url = res_data.get('music')
            
            result = {
                "status": "success",
                "audio": audio_url,
                "type": "video"
            }

            if images:
                result["type"] = "photo"
                result["images"] = images
            else:
                result["sd"] = res_data.get('play')
                result["hd"] = res_data.get('hdplay') or res_data.get('play')

            return jsonify(result)
        else:
            return jsonify({"status": "error", "message": response.get('msg', 'API REJECTED')}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n[+] FOZ GPT ULTRA V4.2 ONLINE")
    print("[+] PHOTO & VIDEO ENGINE ACTIVE")
    app.run(host='0.0.0.0', port=5000, debug=False)
