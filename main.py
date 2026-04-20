import streamlit as st
import base64

# 페이지 설정
st.set_page_config(page_title="소주 갤러그", layout="centered")

# 사진 파일을 Base64로 변환하는 함수 (이미지 미출력 방지 핵심)
def get_image_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# 사진 인코딩
img_base64 = get_image_base64("20260416_130017.jpg")

# 게임 인터페이스 및 로직
st.title("🚀 형을 지켜라! 소주 갤러그")
st.write("방향키로 이동하고 스페이스바로 소주병을 발사하세요!")

# HTML/JS 게임 엔진 (Streamlit 내장)
game_html = f"""
<div id="container" style="position:relative; width:500px; height:600px; background:#000; margin:auto; overflow:hidden; border:5px solid #2ecc71;">
    <canvas id="gCanvas" width="500" height="600"></canvas>
    <div id="ui" style="position:absolute; top:10px; left:10px; color:#0f0; font-family:sans-serif; font-weight:bold;">SCORE: <span id="sc">0</span></div>
</div>

<script>
const canvas = document.getElementById('gCanvas');
const ctx = canvas.getContext('2d');
const scDisp = document.getElementById('sc');

const brotherImg = new Image();
brotherImg.src = "data:image/jpeg;base64,{img_base64}";

let score = 0;
let player = {{ x: 220, y: 500, w: 60, h: 80, tilt: 0 }};
let bullets = [];
let enemies = [];
let keys = {{}};

function spawn() {{
    for(let i=0; i<18; i++) {{
        enemies.push({{ x: (i%6)*70+50, y: Math.floor(i/6)*50+50, w:30, h:30, a:true }});
    }}
}}

window.addEventListener('keydown', e => {{ keys[e.code] = true; if(e.code==='Space') bullets.push({{x:player.x+25, y:player.y, w:10, h:25}}); }});
window.addEventListener('keyup', e => keys[e.code] = false);

function loop() {{
    ctx.fillStyle = '#000';
    ctx.fillRect(0,0,500,600);

    // 플레이어 이동
    if(keys['ArrowLeft'] && player.x > 0) {{ player.x -= 5; player.tilt = -0.2; }}
    else if(keys['ArrowRight'] && player.x < 440) {{ player.x += 5; player.tilt = 0.2; }}
    else {{ player.tilt *= 0.8; }}

    // 형 그리기
    ctx.save();
    ctx.translate(player.x+30, player.y+40);
    ctx.rotate(player.tilt);
    if(brotherImg.src.length > 100) ctx.drawImage(brotherImg, -30, -40, 60, 80);
    else {{ ctx.fillStyle='white'; ctx.fillRect(-30,-40,60,80); }}
    ctx.restore();

    // 총알 및 충돌
    bullets.forEach((b, bi) => {{
        b.y -= 7;
        ctx.fillStyle='#2ecc71'; ctx.fillRect(b.x, b.y, b.w, b.h);
        enemies.forEach(e => {{
            if(e.a && b.x < e.x+e.w && b.x+b.w > e.x && b.y < e.y+e.h && b.y+b.h > e.y) {{
                e.a = false; bullets.splice(bi, 1); score += 100; scDisp.innerText = score;
            }}
        }});
    }});

    // 적 그리기
    enemies.forEach(e => {{ if(e.a) {{ ctx.font="20px Arial"; ctx.fillText("👾", e.x, e.y); }} }});
    if(enemies.length > 0 && enemies.every(e => !e.a)) spawn();

    requestAnimationFrame(loop);
}}
spawn();
loop();
</script>
"""

st.components.v1.html(game_html, height=650)