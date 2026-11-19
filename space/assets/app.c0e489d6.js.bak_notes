
/* ============ 基础：星空 / 时钟 / 导航 ============ */
(function starfield(){
  const cv=document.getElementById('stars'), ctx=cv.getContext('2d');
  let w,h,stars=[];
  function resize(){ w=cv.width=innerWidth; h=cv.height=innerHeight; stars=[]; const n=Math.min(180,Math.floor(w*h/12000));
    for(let i=0;i<n;i++) stars.push({x:Math.random()*w,y:Math.random()*h,z:Math.random()*1.6+.3,r:Math.random()*1.4+.2}); }
  resize(); addEventListener('resize',resize);
  function tick(){ ctx.clearRect(0,0,w,h);
    for(const s of stars){ ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,7); const a=.35+s.z*.4; ctx.fillStyle='rgba(150,200,255,'+a+')'; ctx.fill();
      s.y+=s.z*.18; if(s.y>h){ s.y=-2; s.x=Math.random()*w; } }
    requestAnimationFrame(tick); }
  tick();
})();

/* ============ 流动粒子 ============
   // Motion Prompt #015 Particles · MIT License (c) 2026 Shohei Ohtaki
   // https://showheyohtaki.github.io/motion-prompt/#015
   发射器物理原样搬来：vx ±190 px/s、vy 250–400 px/s 向上、重力 470 px/s²、
   生命 ≤1.5 s、淡入 0.06 s、最后 30% 淡出、缩放 1.15→0.7、圆形/方形/三角、自转 ±4.5 rad/s。
   只做两处改写：发射口从单点改成整条下边缘（环境微粒不该是喷泉），尺寸整体缩到 1.6–4.6 px。
   再加一档「抛体」粒子：带重力，走弧线穿过画面，用来把静止的星野搅活。
   配色守纪律：青为主、冷蓝次之、紫只做少量点缀。 */
(function flowfield(){
  const cv=document.getElementById('flow'); if(!cv) return;
  const ctx=cv.getContext('2d');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const GRAV=470, TAU=Math.PI*2;
  let w=0,h=0,dpr=1,raf=0,last=0,motes=[],acc=0,meteors=[],shot=0.30;

  const PAL=[
    [73,230,255],   /* 青，主色 */
    [73,230,255],
    [150,200,255],  /* 冷蓝 */
    [160,107,255],  /* 紫 */
    [110,255,200],  /* 薄荷 */
    [255,120,180],  /* 玫红，点缀 */
    [255,205,130]   /* 暖橙，点缀 */
  ];
  const SHAPES=['c','c','c','c','s','t'];

  function resize(){
    dpr=Math.min(1.5, devicePixelRatio||1);
    w=innerWidth; h=innerHeight;
    cv.width=Math.round(w*dpr); cv.height=Math.round(h*dpr);
    ctx.setTransform(dpr,0,0,dpr,0,0);
    motes=[]; acc=0; meteors=[];
    const cap=Math.min(58, Math.max(18, Math.floor(w/24)));
    for(let i=0;i<cap;i++) motes.push(spawn(true));
  }

  function spawn(seed){
    const arc = Math.random()<0.18;                 /* 抛体档 */
    const circle = Math.random()<0.72;
    const size = circle ? 1.3+Math.random()*2.1 : 1.8+Math.random()*2.4;
    const col = PAL[Math.floor(Math.random()*PAL.length)];
    return {
      x: Math.random()*w,
      y: seed ? Math.random()*h : h + 6 + Math.random()*10,
      vx: (Math.random()-0.5)*2*190,
      vy: arc ? -(250+Math.random()*150) : -(90+Math.random()*130),
      g: arc ? GRAV : 0,
      r: size,
      life: 0,
      max: arc ? 1.5 : 2.6+Math.random()*2.2,
      a: (arc ? 0.3+Math.random()*0.2 : 0.14+Math.random()*0.24) * (circle?1:0.72),
      rot: Math.random()*TAU,
      spin: (Math.random()-0.5)*2*4.5,
      shape: circle ? 'c' : SHAPES[Math.floor(Math.random()*SHAPES.length)],
      col
    };
  }

  function alphaOf(p){
    const t=p.life/p.max, fin=0.06/p.max;
    if(t<fin) return t/fin;
    if(t>0.7) return (1-t)/0.3;
    return 1;
  }

  function draw(p){
    const t=p.life/p.max, s=1.15-0.45*t, r=p.r*s, a=p.a*alphaOf(p);
    if(a<=0||r<=0) return;
    const c=p.col;
    ctx.save();
    ctx.translate(p.x,p.y);
    if(p.shape==='c'){
      const g=ctx.createRadialGradient(0,0,0,0,0,r*2.6);
      g.addColorStop(0,'rgba('+c[0]+','+c[1]+','+c[2]+','+a+')');
      g.addColorStop(0.42,'rgba('+c[0]+','+c[1]+','+c[2]+','+a*0.42+')');
      g.addColorStop(1,'rgba('+c[0]+','+c[1]+','+c[2]+',0)');
      ctx.fillStyle=g;
      ctx.beginPath(); ctx.arc(0,0,r*2.6,0,TAU); ctx.fill();
    } else {
      ctx.rotate(p.rot);
      ctx.fillStyle='rgba('+c[0]+','+c[1]+','+c[2]+','+a+')';
      if(p.shape==='s'){ ctx.fillRect(-r,-r,r*2,r*2); }
      else {
        ctx.beginPath(); ctx.moveTo(0,-r*1.15);
        ctx.lineTo(r,r*0.72); ctx.lineTo(-r,r*0.72);
        ctx.closePath(); ctx.fill();
      }
    }
    ctx.restore();
  }

  /* ---------- 流星：七彩拖尾 ----------
     一颗流星自己就是一段彩虹：拖尾的渐变沿三个相邻色相走，所以尾巴是渐变的，
     不是单色的一条线。头部亮核用径向白光，外层再垫一片柔光，在 lighter 下自然发光。

     出场位置的关键：**头部必须一出生就在视口里**。之前从 x=-70 起飞，头在屏幕外，
     前 0.4 s 整颗都看不见 —— 命中率全靠运气。现在改成头直接落在画面内、尾巴朝后
     拖在画面里，所以每一颗都是完整可读的一条光。
     头部落在内容层后面也没关系：玻璃面板的 backdrop-filter 会把穿过去的流星糊成
     一道柔光，正好是「流星从舷窗外掠过」的观感。 */
  const HUE=[[255,64,128],[255,150,44],[255,226,64],[74,255,150],[0,208,255],[86,120,255],[178,72,255]];

  function shoot(){
    const k=Math.floor(Math.random()*HUE.length);
    const sp=270+Math.random()*230;                 /* 270–500 px/s：慢慢划过，不是闪一下 */
    const left=Math.random()<0.72;                  /* 七成左→右，三成镜像 */
    const ang=left ? 0.10+Math.random()*0.24 : Math.PI-0.10-Math.random()*0.24;
    const run=430+Math.random()*330;                /* 头这一趟走多远 */
    const len=230+Math.random()*230;                /* 尾巴长度（拖在头后面） */
    /* 关键：头从进到出全程留在画面内 —— 起点按走位反推，并夹在安全边距里。
       以前是「从画外飞进来」，结果大半条命都在画外，静态截图几乎永远抓不到。 */
    const dx=Math.cos(ang)*run, dy=Math.sin(ang)*run;
    const x0=Math.min(Math.max(left ? w*(0.02+Math.random()*0.26) : w*(0.74+Math.random()*0.24),
                               w*0.02), w*0.96-dx);
    /* 两条「看得见」的跑道：玻璃舷窗带（被玻璃折射成柔光）＋ 下方空天区。
       刻意避开中段 0.40–0.70 —— 那里全是实心卡片，画了也被挡住。 */
    const band = Math.random()<0.35 ? [0.24,0.40] : [0.72,0.92];
    const y0=Math.min(Math.max(h*(band[0]+Math.random()*(band[1]-band[0])), h*0.10),
                      h*0.96-Math.abs(dy));
    meteors.push({
      x:x0, y:y0, vx:Math.cos(ang)*sp, vy:Math.sin(ang)*sp,
      len, w:2.3+Math.random()*1.6,
      c0:HUE[k], c1:HUE[(k+1)%HUE.length], c2:HUE[(k+2)%HUE.length], c3:HUE[(k+3)%HUE.length],
      life:0, max:run/sp
    });
  }

  function meteorStep(dt){
    shot-=dt;
    if(shot<=0){ shoot(); if(Math.random()<0.26) shoot(); shot=0.9+Math.random()*1.9; }
    for(let i=meteors.length-1;i>=0;i--){
      const m=meteors[i];
      m.x+=m.vx*dt; m.y+=m.vy*dt; m.life+=dt;
      if(m.life>m.max || m.x<-m.len-80 || m.x>w+80 || m.y<-80 || m.y>h+80){ meteors.splice(i,1); continue; }
      /* 淡入 0.12 s，最后 30% 淡出 */
      const fade=Math.min(1,m.life/0.12)*Math.min(1,(m.max-m.life)/(m.max*0.30));
      const a=fade*0.96;
      const c0=m.c0.join(','), c1=m.c1.join(','), c2=m.c2.join(','), c3=m.c3.join(',');
      ctx.save();
      ctx.translate(m.x,m.y);
      ctx.rotate(Math.atan2(m.vy,m.vx));
      /* 外层柔光：只有这一层用 lighter，它负责「发光」，不负责「颜色」 */
      ctx.globalCompositeOperation='lighter';
      ctx.globalAlpha=0.18*a;
      ctx.fillStyle='rgb('+c1+')';
      ctx.beginPath(); ctx.moveTo(0,-m.w*4.6); ctx.lineTo(-m.len*0.94,0); ctx.lineTo(0,m.w*4.6); ctx.closePath(); ctx.fill();
      /* 主体：必须 source-over 才保得住饱和色相。四个色相沿尾巴依次递进，
         一条尾巴自己就是一段彩虹；若叠在 lighter 下，四色相加又会被洗成奶油白。 */
      ctx.globalCompositeOperation='source-over';
      ctx.globalAlpha=1;
      const g=ctx.createLinearGradient(0,0,-m.len,0);
      g.addColorStop(0,   'rgba('+c0+','+(a*0.98)+')');
      g.addColorStop(0.24,'rgba('+c1+','+(a*0.86)+')');
      g.addColorStop(0.50,'rgba('+c2+','+(a*0.64)+')');
      g.addColorStop(0.76,'rgba('+c3+','+(a*0.34)+')');
      g.addColorStop(1,   'rgba('+c3+',0)');
      ctx.fillStyle=g;
      ctx.beginPath(); ctx.moveTo(0,-m.w*1.15); ctx.lineTo(-m.len,0); ctx.lineTo(0,m.w*1.15); ctx.closePath(); ctx.fill();
      /* 头部：白核压得很小，主色占大面积，读出来才是「彩色流星」而不是白点 */
      const hg=ctx.createRadialGradient(0,0,0,0,0,m.w*5.6);
      hg.addColorStop(0,   'rgba(255,255,255,'+(a*0.90)+')');
      hg.addColorStop(0.16,'rgba('+c0+','+(a*0.86)+')');
      hg.addColorStop(0.46,'rgba('+c0+','+(a*0.34)+')');
      hg.addColorStop(1,   'rgba('+c0+',0)');
      ctx.fillStyle=hg;
      ctx.beginPath(); ctx.arc(0,0,m.w*5.6,0,TAU); ctx.fill();
      ctx.restore();
    }
  }

  function step(dt){
    ctx.clearRect(0,0,w,h);
    ctx.globalCompositeOperation='lighter';
    for(let i=0;i<motes.length;i++){
      const p=motes[i];
      p.life+=dt;
      p.x+=p.vx*dt; p.y+=p.vy*dt; p.vy+=p.g*dt; p.rot+=p.spin*dt;
      if(p.life>=p.max || p.y<-40 || p.x<-60 || p.x>w+60){ motes[i]=spawn(false); continue; }
      draw(p);
    }
    meteorStep(dt);
    ctx.globalCompositeOperation='source-over';
  }

  function tick(now){
    const dt=last ? Math.min(0.05,(now-last)/1000) : 0.016;
    last=now;
    if(!document.hidden && w>0) step(dt);
    raf=requestAnimationFrame(tick);
  }

  resize(); addEventListener('resize',resize);
  if(reduce){ /* 静态一帧，然后停手 */ step(0); }
  else { raf=requestAnimationFrame(tick); }
})();

/* ============ 渐变液态玻璃封面 ============
   // Motion Prompt #095 Animated gradient · MIT License (c) 2026 Shohei Ohtaki
   // https://showheyohtaki.github.io/motion-prompt/#095
   // Motion Prompt #013 Liquid motion   · MIT License (c) 2026 Shohei Ohtaki
   // https://showheyohtaki.github.io/motion-prompt/#013
   #095 的四个径向色块沿椭圆轨道漂移，原周期 4.8 s；封面是背景，慢到 24 s。
   #013 的液态团是「领队 + 7 个拖尾」沿同一条参数曲线、每 0.065 s 递进一格；
   原版靠 blur+alpha 阈值做 goo，这里改用 lighter 叠加：暗底上的同色光斑叠加本身就是液体融并，
   而且不需要离屏画布与 ctx.filter，帧率稳。
   白椭圆高光留着——玻璃的折射感全靠它。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
/* ============ 液态玻璃封面 · 折射层 ============
   画在玻璃面板「后面」（.cover-liquid，z-index 0）：漂移色块 + 球体的体积光。
   这一层会被 .cover-glass 的 backdrop-filter 糊掉，所以只负责「软」的部分；
   脆的棱、水珠、粒子全部交给玻璃表面的 #coverDrops。 */
(function coverLiquid(){
  const host=document.querySelector('.cover');
  const cv=document.getElementById('coverLiquid');
  if(!host||!cv) return;
  const ctx=cv.getContext('2d');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const TAU=Math.PI*2, CYC_BLOB=24, CYC_GOO=9.5;
  let w=0,h=0,dpr=1,raf=0,vis=true;

  /* 玻璃面板在封面里的位置：球的几何全部按玻璃面板算，
     球体才会永远完整地待在玻璃里，不被面板边切掉。 */
  let gx=0,gy=0,gw=0,gh=0;

  /* Motion Prompt #095 · Animated gradient · MIT License (c) 2026 Shohei Ohtaki
     https://showheyohtaki.github.io/motion-prompt/
     四团径向色斑，原始周期 4.8s；这里放慢到 24s 当环境光，且只压右半 —— 左侧是文字区，必须保持暗。 */
  const BLOBS=[
    {cx:.94,cy:.10,ax:.06,ay:.07,rx:.40,ry:.42,sp:1.00,ph:0.0,c:[255,40,110], a:.20},
    {cx:.88,cy:.30,ax:.07,ay:.08,rx:.32,ry:.36,sp:1.22,ph:1.3,c:[255,120,30], a:.20},
    {cx:.72,cy:.16,ax:.06,ay:.06,rx:.28,ry:.30,sp:0.86,ph:2.6,c:[255,225,60], a:.16},
    {cx:.60,cy:.52,ax:.08,ay:.09,rx:.34,ry:.34,sp:1.08,ph:3.9,c:[40,255,170], a:.16},
    {cx:.80,cy:.70,ax:.07,ay:.08,rx:.38,ry:.36,sp:0.94,ph:5.2,c:[0,200,255],  a:.22},
    {cx:.97,cy:.88,ax:.06,ay:.07,rx:.32,ry:.34,sp:1.34,ph:0.7,c:[40,90,255],  a:.22},
    {cx:.66,cy:.92,ax:.07,ay:.06,rx:.36,ry:.30,sp:0.78,ph:4.5,c:[160,60,255], a:.22}
  ];

  function measure(){
    const r=host.getBoundingClientRect();
    if(r.width<2||r.height<2) return false;
    dpr=Math.min(2, devicePixelRatio||1);
    w=Math.round(r.width); h=Math.round(r.height);
    if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){
      cv.width=Math.round(w*dpr); cv.height=Math.round(h*dpr);
      ctx.setTransform(dpr,0,0,dpr,0,0);
    }
    const g=document.querySelector('.cover-glass');
    if(g){
      const gr=g.getBoundingClientRect();
      gx=gr.left-r.left; gy=gr.top-r.top; gw=gr.width; gh=gr.height;
    } else { gx=0; gy=0; gw=w; gh=h; }
    return true;
  }

  function radial(x,y,r,c,a){
    const g=ctx.createRadialGradient(x,y,0,x,y,r);
    g.addColorStop(0,   'rgba('+c[0]+','+c[1]+','+c[2]+','+a+')');
    g.addColorStop(0.34,'rgba('+c[0]+','+c[1]+','+c[2]+','+(a*0.62)+')');
    g.addColorStop(0.68,'rgba('+c[0]+','+c[1]+','+c[2]+','+(a*0.2)+')');
    g.addColorStop(1,   'rgba('+c[0]+','+c[1]+','+c[2]+',0)');
    ctx.fillStyle=g;
    ctx.beginPath(); ctx.arc(x,y,r,0,TAU); ctx.fill();
  }

  /* 球轨道：与 #coverDrops 用同一套公式（同一个 CYC_GOO、同一个绝对时间），两层才严丝合缝 */
  function orbs(t){
    const baseR=Math.max(22,Math.min(gh*0.33,gw*0.155));
    const clX=function(x,r){ return Math.min(gw-r*1.06,Math.max(r*1.06,x)); };
    const clY=function(y,r){ return Math.min(gh-r*1.12,Math.max(r*1.02,y)); };
    /* 窄屏：面板只有 340px 宽，大球没地方活 —— 缩成右上角一颗玻璃弹珠，
       和 chip 抢位置的问题直接消失。 */
    const nar=gw<560;
    const A={r:nar?baseR*0.66:baseR};
    A.x=gx+clX(gw*((nar?0.92:0.70)+(nar?0.05:0.15)*Math.sin(t/CYC_GOO*TAU*1.05+0.3)),A.r);
    A.y=gy+clY(gh*((nar?0.14:0.50)+(nar?0.06:0.24)*Math.cos(t/CYC_GOO*TAU*0.88)),A.r);
    const B={r:baseR*0.44};
    B.x=gx+clX(gw*(0.80+0.08*Math.sin(t/CYC_GOO*TAU*0.72+2.4)),B.r);
    B.y=gy+clY(gh*(0.78+0.18*Math.cos(t/CYC_GOO*TAU*1.13+1.1)),B.r);
    const C={r:baseR*0.32};
    C.x=gx+clX(gw*(0.55+0.12*Math.sin(t/CYC_GOO*TAU*1.31+4.1)),C.r);
    C.y=gy+clY(gh*(0.26+0.14*Math.cos(t/CYC_GOO*TAU*0.67+2.7)),C.r);
    return {A:A,B:B,C:C};
  }

  function frame(t){
    if(!measure()) return;

    /* 底：深空渐变，保证玻璃后面永远有东西可透 */
    const base=ctx.createLinearGradient(0,0,w,h);
    base.addColorStop(0,'#05070f');
    base.addColorStop(0.55,'#070b18');
    base.addColorStop(1,'#04060d');
    ctx.fillStyle=base; ctx.fillRect(0,0,w,h);

    /* 彩虹膜：一条饱和光谱用 source-over 直接铺上去。
       用 lighter 叠只会越叠越白（上一版就是这样糊成奶油的），
       source-over 才有真正的色相，玻璃的「薄膜干涉」也才有读法。 */
    const film=ctx.createLinearGradient(w*0.08,h*0.96,w*0.99,h*0.04);
    /* 每一档都用纯色相：中间调的绿+黄只要饱和度不够就会混成橄榄泥，
       纯色相的绿和纯色相的黄叠出来才是亮柠檬。 */
    film.addColorStop(0.00,'rgba(120,0,255,0.52)');
    film.addColorStop(0.13,'rgba(40,60,255,0.52)');
    film.addColorStop(0.26,'rgba(0,200,255,0.50)');
    film.addColorStop(0.38,'rgba(0,255,150,0.46)');
    film.addColorStop(0.50,'rgba(220,255,0,0.38)');
    film.addColorStop(0.62,'rgba(255,180,0,0.42)');
    film.addColorStop(0.74,'rgba(255,80,60,0.46)');
    film.addColorStop(0.86,'rgba(255,40,140,0.50)');
    film.addColorStop(1.00,'rgba(190,40,255,0.52)');
    ctx.fillStyle=film; ctx.fillRect(0,0,w,h);

    /* 第二层薄膜，反向斜穿、半透，让色相交叉而不是排成一条 */
    ctx.save();
    ctx.globalAlpha=0.22;
    const film2=ctx.createLinearGradient(w*0.92,h*0.98,w*0.12,h*0.06);
    film2.addColorStop(0.00,'rgba(255,40,120,0.6)');
    film2.addColorStop(0.25,'rgba(255,200,0,0.5)');
    film2.addColorStop(0.50,'rgba(0,255,180,0.45)');
    film2.addColorStop(0.75,'rgba(0,140,255,0.5)');
    film2.addColorStop(1.00,'rgba(140,60,255,0.6)');
    ctx.fillStyle=film2; ctx.fillRect(0,0,w,h);
    ctx.restore();

    ctx.globalCompositeOperation='lighter';
    /* 静态锚点：漂移色块会随周期忽明忽暗，垫一层不动的光，封面任何时刻都不塌 */
    radial(w*0.86,h*0.62,Math.max(w,h)*0.62,[0,190,255],0.16);
    radial(w*0.99,h*0.14,Math.max(w,h)*0.46,[150,70,255],0.16);

    for(const b of BLOBS){
      const u=(t/CYC_BLOB)*TAU*b.sp+b.ph;
      const x=(b.cx+Math.cos(u)*b.ax)*w;
      const y=(b.cy+Math.sin(u*1.07)*b.ay)*h;
      const breathe=1+Math.sin(u*1.6+b.ph)*0.09;
      radial(x,y,Math.max(w,b.rx*w)*b.rx*breathe,b.c,b.a);
    }

    const gr=Math.min(w,h);
    const damp=w<560?0.78:1;
    const o=orbs(t);

    /* 球后面的色雾：让球浮在光里，也给 backdrop-filter 一点可采样的内容 */
    radial(o.A.x,o.A.y,o.A.r*3.2,[160,107,255],0.26*damp);
    radial(o.A.x,o.A.y,o.A.r*2.0,[59,123,255], 0.30*damp);
    radial(o.B.x,o.B.y,o.B.r*1.8,[73,230,255], 0.22*damp);

    /* 实体球不画在这层 —— 糊过之后只剩一团光。这里只留「球在玻璃后面透出来的光」，
       把体积感垫出来；脆棱交给玻璃表面的 #coverDrops。 */
    radial(o.A.x,o.A.y,o.A.r*1.25,[73,230,255], 0.26*damp);
    radial(o.B.x,o.B.y,o.B.r*1.9, [124,112,255],0.2*damp);
    radial(o.C.x,o.C.y,o.C.r*2.1, [130,240,255],0.13*damp);

    /* 白椭圆：玻璃的折射点，同样只放右半，别压字 */
    const hx=w*(0.66+0.10*Math.sin(t/CYC_BLOB*TAU));
    const hy=h*(0.26+0.06*Math.cos(t/CYC_BLOB*TAU*1.2));
    ctx.save();
    ctx.translate(hx,hy); ctx.rotate(-0.42); ctx.scale(1.9,0.8);
    const hg=ctx.createRadialGradient(0,0,0,0,0,Math.max(28,gr*0.3));
    hg.addColorStop(0,'rgba(255,255,255,0.16)');
    hg.addColorStop(0.5,'rgba(255,255,255,0.05)');
    hg.addColorStop(1,'rgba(255,255,255,0)');
    ctx.fillStyle=hg;
    ctx.beginPath(); ctx.arc(0,0,Math.max(28,gr*0.3),0,TAU); ctx.fill();
    ctx.restore();

    ctx.globalCompositeOperation='source-over';

    /* 边缘加深：玻璃有厚度，四周必须比中心暗，否则整块面板会飘起来 */
    const vig=ctx.createRadialGradient(w*0.66,h*0.52,Math.min(w,h)*0.18,w*0.66,h*0.52,Math.max(w,h)*0.92);
    vig.addColorStop(0,'rgba(4,6,13,0)');
    vig.addColorStop(0.6,'rgba(4,6,13,0.16)');
    vig.addColorStop(1,'rgba(4,6,13,0.52)');
    ctx.fillStyle=vig; ctx.fillRect(0,0,w,h);
  }

  function tick(now){
    /* 绝对时间：水珠层要用同一套几何算球棱，两层的 t 必须一致 */
    if(!document.hidden && vis) frame(now/1000);
    raf=requestAnimationFrame(tick);
  }
  function start(){ if(!raf) raf=requestAnimationFrame(tick); }
  function stop(){ if(raf){ cancelAnimationFrame(raf); raf=0; } }

  const dash=host.closest('.view');
  if(dash && 'IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      vis=es[0].isIntersecting;
      if(vis){ measure(); start(); } else { stop(); }
    },{threshold:0.02}).observe(host);
  }
  if('ResizeObserver' in window){ new ResizeObserver(function(){ if(vis) frame(performance.now()/1000); }).observe(host); }
  addEventListener('resize',function(){ if(vis) frame(performance.now()/1000); });

  measure();
  if(reduce){ frame(1.2); } else { start(); }
})();

/* ============ 液态玻璃封面 · 表面层 ============
   画在玻璃面板「之上」（.cover-glass 的第一个子节点），不受 backdrop-filter 影响：
   所以棱是脆的、高光是实的 —— 这才是「液态玻璃」该有的读法。
   这层只画三样：漂移粒子、表面水珠、一枚主透镜。 */
(function coverDrops(){
  const host=document.querySelector('.cover-glass');
  const cv=document.getElementById('coverDrops');
  if(!host||!cv) return;
  const ctx=cv.getContext('2d');
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const TAU=Math.PI*2, CYC_GOO=9.5;
  let w=0,h=0,dpr=1,raf=0,vis=true;

  /* 每颗水珠：位置（归一化）、半径（px 基准）、相位、漂移幅度、形变种子 */
  const BEADS=[
    {x:.66,y:.18,r:11.0,ph:0.0,amp:0.010,seed:0.7},
    {x:.84,y:.62,r:9.0, ph:1.9,amp:0.013,seed:2.4},
    {x:.63,y:.72,r:6.5, ph:3.4,amp:0.016,seed:4.1},
    {x:.91,y:.24,r:5.5, ph:5.1,amp:0.012,seed:1.3},
    {x:.78,y:.88,r:4.6, ph:2.6,amp:0.018,seed:3.7},
    {x:.55,y:.72,r:3.8, ph:4.4,amp:0.020,seed:5.5},
    {x:.95,y:.80,r:3.2, ph:0.9,amp:0.015,seed:0.2}
  ];

  function measure(){
    const r=host.getBoundingClientRect();
    if(r.width<2||r.height<2) return false;
    dpr=Math.min(2,devicePixelRatio||1);
    w=Math.round(r.width); h=Math.round(r.height);
    if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){
      cv.width=Math.round(w*dpr); cv.height=Math.round(h*dpr);
      ctx.setTransform(dpr,0,0,dpr,0,0);
    }
    return true;
  }

  /* 球轨道：与 coverLiquid 同一套公式，只是这里画布就是玻璃面板本身，不需要 gx/gy */
  function orbs(t){
    const baseR=Math.max(22,Math.min(h*0.33,w*0.155));
    const clX=function(x,r){ return Math.min(w-r*1.06,Math.max(r*1.06,x)); };
    const clY=function(y,r){ return Math.min(h-r*1.12,Math.max(r*1.02,y)); };
    const nar=w<560;
    const A={r:nar?baseR*0.66:baseR};
    A.x=clX(w*((nar?0.92:0.70)+(nar?0.05:0.15)*Math.sin(t/CYC_GOO*TAU*1.05+0.3)),A.r);
    A.y=clY(h*((nar?0.14:0.50)+(nar?0.06:0.24)*Math.cos(t/CYC_GOO*TAU*0.88)),A.r);
    return {A:A};
  }

  /* 同一条轮廓，按 k 缩放：棱、镜面、焦散全部长在同一条曲线上，
     否则圆椭圆一混用，球上就会多出一道对不齐的「钩子」。 */
  function shape(cx,cy,R,seed,k){
    const N=96, sc=(k===undefined?1:k);
    ctx.beginPath();
    for(let i=0;i<=N;i++){
      const th=i/N*TAU;
      const rr=R*sc*(1
        +0.042*Math.sin(th*2+seed*1.7)
        +0.030*Math.sin(th*3-seed*2.3)
        +0.016*Math.sin(th*5+seed*0.9));
      const x=cx+Math.cos(th)*rr*1.06;
      const y=cy+Math.sin(th)*rr*0.9;
      if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    }
    ctx.closePath();
  }

  /* 开弧版：焦散只许画在球的下半圈 */
  function shapeArc(cx,cy,R,seed,k,a0,a1){
    const N=72, sc=(k===undefined?1:k);
    ctx.beginPath();
    for(let i=0;i<=N;i++){
      const th=a0+(a1-a0)*i/N;
      const rr=R*sc*(1
        +0.042*Math.sin(th*2+seed*1.7)
        +0.030*Math.sin(th*3-seed*2.3)
        +0.016*Math.sin(th*5+seed*0.9));
      const x=cx+Math.cos(th)*rr*1.06;
      const y=cy+Math.sin(th)*rr*0.9;
      if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    }
  }

  /* 液态玻璃球（实体版）：这层在玻璃「之上」，不会被糊，所以棱是脆的。
     ① 体：亮透镜 —— 球体要比面板「透光」，才像光穿过一块厚玻璃
     ② 内壁暗环（玻璃厚度）+ 左上透光 ③ 左上镜面柔光斑 ④ 底部焦散 ⑤ 菲涅尔细棱 */
  function droplet(cx,cy,R,seed,c1,c2,a){
    shape(cx,cy,R,seed,1);
    const g=ctx.createLinearGradient(cx-R*0.7,cy-R*0.95,cx+R*0.8,cy+R*0.85);
    g.addColorStop(0,   'rgba(236,250,255,'+(a*0.11)+')');
    g.addColorStop(0.28,'rgba(255,196,220,'+(a*0.05)+')');
    g.addColorStop(0.50,'rgba(190,255,236,'+(a*0.04)+')');
    g.addColorStop(0.72,'rgba(198,214,255,'+(a*0.05)+')');
    g.addColorStop(1,   'rgba(236,250,255,'+(a*0.13)+')');
    ctx.fillStyle=g; ctx.fill();

    ctx.save();
    shape(cx,cy,R,seed,1); ctx.clip();

    const wall=ctx.createRadialGradient(cx+R*0.12,cy+R*0.16,R*0.42,cx+R*0.12,cy+R*0.16,R*1.16);
    wall.addColorStop(0,   'rgba(4,8,18,0)');
    wall.addColorStop(0.72,'rgba(4,8,18,'+(a*0.10)+')');
    wall.addColorStop(1,   'rgba(4,8,18,'+(a*0.34)+')');
    ctx.fillStyle=wall; ctx.fillRect(cx-R*1.5,cy-R*1.5,R*3,R*3);

    const lit=ctx.createRadialGradient(cx-R*0.3,cy-R*0.4,0,cx-R*0.3,cy-R*0.4,R*0.86);
    lit.addColorStop(0,   'rgba(222,252,255,'+(a*0.18)+')');
    lit.addColorStop(0.45,'rgba(222,252,255,'+(a*0.08)+')');
    lit.addColorStop(1,   'rgba(222,252,255,0)');
    ctx.fillStyle=lit; ctx.fillRect(cx-R*1.5,cy-R*1.5,R*3,R*3);

    /* 镜面：不描线，改成贴在左上内壁的柔光斑 —— 描线怎么叠都会留下「双轮廓」，光斑不会 */
    const hx=cx-R*0.34, hy=cy-R*0.40;
    ctx.save();
    ctx.translate(hx,hy); ctx.rotate(-0.55); ctx.scale(1.55,0.78);
    const hg=ctx.createRadialGradient(0,0,0,0,0,R*0.72);
    hg.addColorStop(0,   'rgba(252,255,255,'+(a*0.50)+')');
    hg.addColorStop(0.34,'rgba(240,254,255,'+(a*0.20)+')');
    hg.addColorStop(0.68,'rgba(226,250,255,'+(a*0.05)+')');
    hg.addColorStop(1,   'rgba(226,250,255,0)');
    ctx.fillStyle=hg;
    ctx.beginPath(); ctx.arc(0,0,R*0.72,0,TAU); ctx.fill();
    ctx.restore();

    /* 底部焦散：只画下半圈，两端靠径向衰减收掉，不会在弧端切一刀 */
    const cg=ctx.createRadialGradient(cx,cy+R*0.72,0,cx,cy+R*0.72,R*0.86);
    cg.addColorStop(0,   'rgba(200,255,240,'+(a*0.72)+')');
    cg.addColorStop(0.55,'rgba(150,235,255,'+(a*0.42)+')');
    cg.addColorStop(1,   'rgba(200,180,255,0)');
    shapeArc(cx,cy,R,seed,0.87,Math.PI*0.16,Math.PI*0.84);
    ctx.strokeStyle=cg;
    ctx.lineWidth=Math.max(1.2,R*0.05); ctx.stroke();

    ctx.restore();

    /* 菲涅尔细棱：一条线就够 */
    shape(cx,cy,R,seed,1);
    const rg=ctx.createLinearGradient(cx-R*0.9,cy-R*0.9,cx+R*0.9,cy+R*0.9);
    rg.addColorStop(0,   'rgba(255,246,252,'+(a*0.52)+')');
    rg.addColorStop(0.28,'rgba(255,170,150,'+(a*0.24)+')');
    rg.addColorStop(0.50,'rgba(190,255,230,'+(a*0.22)+')');
    rg.addColorStop(0.74,'rgba(120,200,255,'+(a*0.24)+')');
    rg.addColorStop(1,   'rgba(186,140,255,'+(a*0.48)+')');
    ctx.strokeStyle=rg;
    ctx.lineWidth=0.9; ctx.stroke();
  }

  /* 内部镜面高光：玻璃球的反射点，永远朝左上 */
  function spec(cx,cy,R,a){
    ctx.save();
    ctx.translate(cx-R*0.3,cy-R*0.34);
    ctx.rotate(-0.5);
    const g=ctx.createRadialGradient(0,0,0,0,0,R*0.6);
    g.addColorStop(0,'rgba(255,255,255,'+a+')');
    g.addColorStop(0.42,'rgba(232,250,255,'+(a*0.28)+')');
    g.addColorStop(1,'rgba(232,250,255,0)');
    ctx.fillStyle=g;
    ctx.scale(1.6,0.72);
    ctx.beginPath(); ctx.arc(0,0,R*0.6,0,TAU); ctx.fill();
    ctx.restore();
  }

  /* 一颗水珠：① 上亮下暗的球体 ② 一圈脆棱 ③ 底部焦散弧 ④ 左上高光点 */
  function bead(cx,cy,R,seed){
    const N=48;
    ctx.beginPath();
    for(let i=0;i<=N;i++){
      const th=i/N*TAU;
      const rr=R*(1+0.045*Math.sin(th*3+seed*2.1)+0.03*Math.sin(th*5-seed*1.4));
      const x=cx+Math.cos(th)*rr, y=cy+Math.sin(th)*rr*0.94;
      if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    }
    ctx.closePath();
    const g=ctx.createLinearGradient(cx-R*.7,cy-R*.8,cx+R*.6,cy+R*.8);
    g.addColorStop(0,'rgba(255,255,255,0.34)');
    g.addColorStop(0.42,'rgba(198,236,255,0.14)');
    g.addColorStop(0.78,'rgba(120,160,255,0.12)');
    g.addColorStop(1,'rgba(8,12,26,0.30)');
    ctx.fillStyle=g; ctx.fill();

    ctx.strokeStyle='rgba(236,252,255,0.58)';
    ctx.lineWidth=Math.max(0.8,R*0.075); ctx.stroke();

    ctx.beginPath();
    ctx.arc(cx,cy,R*0.78,Math.PI*0.22,Math.PI*0.78);
    ctx.strokeStyle='rgba(180,240,255,0.5)';
    ctx.lineWidth=Math.max(0.7,R*0.06); ctx.stroke();

    const sx=cx-R*0.34, sy=cy-R*0.38, sr=Math.max(0.9,R*0.26);
    const sg=ctx.createRadialGradient(sx,sy,0,sx,sy,sr);
    sg.addColorStop(0,'rgba(255,255,255,0.95)');
    sg.addColorStop(1,'rgba(255,255,255,0)');
    ctx.fillStyle=sg;
    ctx.beginPath(); ctx.arc(sx,sy,sr,0,TAU); ctx.fill();
  }

  /* 封面里自己的流动粒子：小、慢、往上飘，和全站 #flow 同一个物理手感
     （Motion Prompt #015 · 发射器 + 重力 + 末段淡出），只是半径更小、光更软。 */
  const MOTES=[];
  const MOTE_N=26;
  const MOTE_C=[[73,230,255],[110,255,200],[150,200,255],[170,110,255],[255,120,180],[255,205,130],[120,255,235]];
  for(let i=0;i<MOTE_N;i++){
    MOTES.push({
      u:Math.random(),
      v:Math.random(),
      r:0.8+Math.random()*1.5,
      sp:0.014+Math.random()*0.026,
      sw:0.004+Math.random()*0.012,
      ph:Math.random()*TAU,
      c:MOTE_C[i%MOTE_C.length],
      a:0.25+Math.random()*0.4
    });
  }

  function mote(m,t){
    const y=((m.v-t*m.sp)%1+1)%1;                 /* 上浮并循环 */
    const x=((m.u+Math.sin(t*0.6+m.ph)*m.sw)%1+1)%1;
    const px=x*w, py=y*h;
    const fade=Math.min(1, y*4)*Math.min(1,(1-y)*3.4);  /* 两端淡出，不出现硬切 */
    const a=m.a*fade;
    if(a<=0.01) return;
    const R=m.r*(1+0.25*Math.sin(t*2.2+m.ph));
    const g=ctx.createRadialGradient(px,py,0,px,py,R*3.2);
    g.addColorStop(0,'rgba('+m.c[0]+','+m.c[1]+','+m.c[2]+','+a+')');
    g.addColorStop(0.4,'rgba('+m.c[0]+','+m.c[1]+','+m.c[2]+','+(a*0.3)+')');
    g.addColorStop(1,'rgba('+m.c[0]+','+m.c[1]+','+m.c[2]+',0)');
    ctx.fillStyle=g;
    ctx.beginPath(); ctx.arc(px,py,R*3.2,0,TAU); ctx.fill();
  }

  function frame(t){
    if(!measure()) return;
    ctx.clearRect(0,0,w,h);

    const narrow=w<560;
    const scale=narrow?0.82:1;

    for(const m of MOTES) mote(m,t);

    if(w>2&&h>2){
      const o=orbs(t);
      /* 只放一枚主透镜：小尺度的细节交给水珠和粒子，多一个球只会互相抢 */
      droplet(o.A.x,o.A.y,o.A.r,0.6,[73,230,255],[126,92,255],0.78*scale);
      spec(o.A.x,o.A.y,o.A.r,0.42*scale);
    }

    for(const b of BEADS){
      const u=t*0.55+b.ph;
      const x=w*(b.x+Math.sin(u)*b.amp*3);
      const y=h*(b.y+Math.cos(u*0.83)*b.amp*2.2);
      const R=b.r*scale*(0.94+0.06*Math.sin(u*1.7));
      if(x<0||x>w||y<0||y>h) continue;
      bead(x,y,R,b.seed);
    }
  }

  function tick(now){
    if(!document.hidden && vis) frame(now/1000);
    raf=requestAnimationFrame(tick);
  }
  function start(){ if(!raf) raf=requestAnimationFrame(tick); }
  function stop(){ if(raf){ cancelAnimationFrame(raf); raf=0; } }

  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      vis=es[0].isIntersecting;
      if(vis){ measure(); start(); } else { stop(); }
    },{threshold:0.02}).observe(host);
  }
  if('ResizeObserver' in window){ new ResizeObserver(function(){ if(vis) frame(performance.now()/1000); }).observe(host); }
  addEventListener('resize',function(){ if(vis) frame(performance.now()/1000); });

  measure();
  if(reduce){ frame(1.2); } else { start(); }
})();
function pad(n){ return String(n).padStart(2,'0'); }
function updateClock(){ const d=new Date(); document.getElementById('clock').textContent=`${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; }
setInterval(updateClock,1000); updateClock();
document.getElementById('year').textContent=new Date().getFullYear();

const startTs=Date.now();
setInterval(()=>{ document.getElementById('statUptime').textContent=Math.floor((Date.now()-startTs)/60000); },5000);

/* nav */
const nav=document.getElementById('nav');
function showView(v){
  document.querySelectorAll('.view').forEach(s=>s.classList.remove('active'));
  document.getElementById('view-'+v).classList.add('active');
  nav.querySelectorAll('button').forEach(b=>b.classList.toggle('active', b.dataset.view===v));
  window.scrollTo({top:0,behavior:'smooth'});
  try{ history.replaceState(null,'','#'+v); document.title=({dash:'🚀 驾驶舱',games:'🎮 小游戏',notes:'📚 资料库',board:'💬 留言板',ai:'🤖 AI助手',about:'✨ 关于'}[v]||'XS 空间站')+' · XS 空间站'; }catch(e){}
}
// 首次加载：支持 #位置 / 页面视图直达
(function(){
  const m=(location.hash||'').replace('#','').trim();
  if(m && document.getElementById('view-'+m)) showView(m);
})();
nav.addEventListener('click',e=>{ const b=e.target.closest('button[data-view]'); if(b) showView(b.dataset.view); });
document.getElementById('quick').addEventListener('click',e=>{ const b=e.target.closest('button[data-go]'); if(b) showView(b.dataset.go); });
// 快捷键：`/` 聚焦搜索（资料库页）、`g` + 方向跳转、Esc 关弹窗
document.addEventListener('keydown',(e)=>{
  const tag=(e.target.tagName||'').toLowerCase();
  if(tag==='input'||tag==='textarea') return;
  if(e.key==='/'){
    const s=document.getElementById('noteSearch');
    if(s && document.getElementById('view-notes').classList.contains('active')){ e.preventDefault(); s.focus(); }
  } else if(e.key==='Escape'){
    closeGame();
  } else if(e.key==='g'){
    // g 有争议，改用 F 打开游戏、B 打开留言板、A 打开AI
  } else if(e.key==='f'){ showView('games'); }
  else if(e.key==='b'){ showView('board'); }
  else if(e.key==='n'){ showView('notes'); }
  else if(e.key==='a'){ showView('ai'); }
  else if(e.key==='h'||e.key==='H'){ showView('dash'); }
});

/* ============ 数据层：本机优先（localStorage）+ 可选云同步 ============
 * 所有功能在断网或后端不可达时 100% 可用；云端只作为可选的跨设备同步通道，
 * 默认关闭，且不再把任何凭据写死在前端源码里。
 * 开启云同步：浏览器控制台执行
 *   localStorage.setItem('xs_cloud_config', JSON.stringify({url:'https://<可达域名>', key:'<anon key>'}))
 * 然后刷新；留空或删除该项即关闭。
 */
const LS = {
  notes: 'xs_space_notes_v1', messages: 'xs_space_messages_v1',
  visits: 'xs_space_visits_v1', files: 'xs_space_files_v1', cloud: 'xs_cloud_config'
};
function esc(s){ return String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function readJSON(k,fb){ try{ const v=JSON.parse(localStorage.getItem(k)); return (v===null||v===undefined)?fb:v; }catch(e){ return fb; } }
function writeJSON(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); return true; }catch(e){ return false; } }
function uid(){ return 'l-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,7); }
function readCloud(){
  try{
    const c=JSON.parse(localStorage.getItem(LS.cloud)||'null');
    if(c && /^https:\/\//.test(c.url||'') && c.key) return {base:String(c.url).replace(/\/+$/,''), key:String(c.key)};
  }catch(e){}
  return null;
}
let CLOUD = readCloud();
function cloudTable(t){ return CLOUD ? CLOUD.base+'/rest/v1/'+t : null; }
function cloudHeaders(extra){ return Object.assign({apikey:CLOUD.key,Authorization:'Bearer '+CLOUD.key},extra||{}); }
async function fetchT(url,opts,ms){
  const c=new AbortController(); const timer=setTimeout(()=>c.abort(),ms||6000);
  try{ return await fetch(url,Object.assign({},opts,{signal:c.signal})); }
  finally{ clearTimeout(timer); }
}
// 云端写入永远 best-effort：失败静默，本机数据已经落盘
async function cloudPush(table,method,body,filter){
  if(!CLOUD) return;
  let url=cloudTable(table); if(filter) url+='?id=eq.'+encodeURIComponent(filter);
  try{ await fetchT(url,{method,headers:cloudHeaders({'Content-Type':'application/json'}),body:body?JSON.stringify(body):undefined},6000); }catch(e){}
}
function setSrc(t){ const el=document.getElementById('noteSource'); if(el) el.textContent=t; }
function mountCloudButton(){
  const host=document.getElementById('noteHint'); if(!host||document.getElementById('cloudBtn')) return;
  const b=document.createElement('button'); b.id='cloudBtn'; b.type='button';
  b.className='btn ghost'; b.style.cssText='margin-left:10px;padding:3px 10px;font-size:11px';
  b.textContent=CLOUD?'云同步：开':'云同步：关';
  b.setAttribute('aria-label','配置可选的跨设备云同步');
  b.addEventListener('click',()=>{
    const cur=localStorage.getItem(LS.cloud)||'';
    const v=prompt('可选：填写云同步配置 JSON（留空关闭云同步）。\n格式：{"url":"https://可达域名","key":"anon key"}',cur);
    if(v===null) return;
    if(!v.trim()){ localStorage.removeItem(LS.cloud); }
    else {
      try{ JSON.parse(v.trim()); }catch(e){ alert('配置不是合法 JSON，已忽略'); return; }
      localStorage.setItem(LS.cloud,v.trim());
    }
    CLOUD=readCloud(); loadNotes(); loadMessages(); loadFiles();
    const old=document.getElementById('cloudBtn'); if(old) old.remove(); mountCloudButton();
  });
  host.appendChild(b);
}

/* ---------- 资料库 ---------- */
let notesCache=[]; let noteQuery=''; let noteCatFilter='';
function loadNotes(){
  notesCache=readJSON(LS.notes,[]); if(!Array.isArray(notesCache)) notesCache=[];
  setSrc(CLOUD?'本机 + 云同步':'本机存储');
  renderNotes();
  if(CLOUD) syncNotes();
}
async function syncNotes(){
  try{
    const r=await fetchT(cloudTable('notes')+'?select=*&order=ts.desc',{headers:cloudHeaders()},8000);
    if(!r.ok) throw new Error('HTTP '+r.status);
    const remote=await r.json();
    if(!Array.isArray(remote)) throw new Error('云端数据格式异常');
    const seen=new Set(notesCache.map(n=>String(n.id)));
    const merged=notesCache.slice();
    remote.forEach(n=>{ if(n&&!seen.has(String(n.id))){ merged.push(n); seen.add(String(n.id)); } });
    merged.sort((x,y)=>(y.ts||0)-(x.ts||0));
    notesCache=merged; writeJSON(LS.notes,notesCache);
    // 本机独有记录回传云端（best-effort）
    const remoteIds=new Set(remote.map(n=>String(n.id)));
    notesCache.filter(n=>String(n.id).indexOf('l-')===0 && !remoteIds.has(String(n.id)))
      .slice(0,20).forEach(n=>cloudPush('notes','POST',{title:n.title,body:n.body,cat:n.cat,ts:n.ts}));
    setSrc('本机 + 云同步'); renderNotes();
  }catch(e){ setSrc('本机存储（云同步暂不可用）'); }
}
function renderNotes(){
  const q=noteQuery.trim().toLowerCase(), cf=noteCatFilter;
  const arr=notesCache.filter(n=>{
    if(cf && (n.cat||'笔记')!==cf) return false;
    if(q && !(String(n.title||'').toLowerCase().includes(q)||String(n.body||'').toLowerCase().includes(q))) return false;
    return true;
  });
  const box=document.getElementById('noteList'); box.innerHTML='';
  document.getElementById('statNotes').textContent=notesCache.length;
  if(!arr.length){ box.innerHTML='<div class="small dim">没有匹配的资料。可在上方新增一条。</div>'; return; }
  arr.forEach(n=>{
    const body=String(n.body||''), isLink=/^https?:\/\//i.test(body.trim()), cat=n.cat||'笔记';
    const el=document.createElement('div'); el.className='note-item';
    el.innerHTML='<button class="del" data-id="'+esc(n.id)+'" aria-label="删除这条资料" title="删除">🗑</button>'+
      '<h4>'+esc(n.title||'(无标题)')+' <span class="type">'+esc(cat)+'</span></h4>'+
      (isLink?'<p><a href="'+esc(body.trim())+'" target="_blank" rel="noopener" style="color:var(--cyan)">'+esc(body.trim())+'</a></p>':'<p>'+esc(body)+'</p>');
    box.appendChild(el);
  });
}
function addNote(){
  const t=document.getElementById('noteTitle').value.trim(), b=document.getElementById('noteBody').value.trim();
  if(!t&&!b) return;
  const rec={id:uid(),title:t,body:b,cat:document.getElementById('noteCat').value||'笔记',ts:Date.now()};
  notesCache=[rec,...notesCache];
  const ok=writeJSON(LS.notes,notesCache);
  if(CLOUD) cloudPush('notes','POST',{title:rec.title,body:rec.body,cat:rec.cat,ts:rec.ts});
  setSrc(ok?'本机存储'+(CLOUD?' + 云同步':'（空间不足，未保存）'):'本机存储');
  document.getElementById('noteTitle').value=''; document.getElementById('noteBody').value='';
  renderNotes();
}
function delNote(id){
  const n=notesCache.find(x=>String(x.id)===String(id));
  notesCache=notesCache.filter(x=>String(x.id)!==String(id));
  writeJSON(LS.notes,notesCache);
  if(n&&CLOUD&&String(n.id).indexOf('l-')!==0) cloudPush('notes','DELETE',null,id);
  renderNotes();
}
document.getElementById('addNote').addEventListener('click',addNote);
document.getElementById('noteList').addEventListener('click',e=>{ const d=e.target.closest('.del'); if(d) delNote(d.dataset.id); });
document.getElementById('noteSearch').addEventListener('input',e=>{ noteQuery=e.target.value; renderNotes(); });
document.getElementById('noteFilter').addEventListener('change',e=>{ noteCatFilter=e.target.value; renderNotes(); });

/* ---------- 文件区：本机上传 + 仓库静态资源 + 可选云 ---------- */
const FILE_PREFIX='__file__';
function staticPath(p){
  const raw=String(p||'');
  if(raw.indexOf('resources/')===0) return '../'+raw;   // 页面位于 /space/ 下
  if(raw.indexOf('/')===0) return raw;
  return '../resources/'+raw.replace(/^.*\//,'');
}
async function loadFiles(){
  const box=document.getElementById('fileList');
  let items=readJSON(LS.files,[]);
  if(!Array.isArray(items)) items=[];
  items=items.map(f=>({name:f.name,data:f.data,id:f.id,source:'本机'}));
  try{
    const r=await fetchT('../resources/index.json',{},5000);
    if(r.ok){ const local=await r.json(); (Array.isArray(local)?local:[]).forEach(f=>items.push({name:f.name||f.path,path:staticPath(f.path),desc:f.desc,source:'仓库'})); }
  }catch(e){}
  if(CLOUD){
    try{
      const r=await fetchT(cloudTable('messages')+'?select=*&order=ts.desc',{headers:cloudHeaders()},8000);
      if(r.ok){ const all=await r.json(); (Array.isArray(all)?all:[]).filter(x=>String(x.name||'').indexOf(FILE_PREFIX)===0).forEach(c=>{
        let name=c.body||'file', data=null;
        try{ const j=JSON.parse(c.body||''); if(j&&j.name){ name=j.name; data=j.data; } }catch(e){}
        items.push({name,data,id:c.id,source:'云端'});
      }); }
    }catch(e){}
  }
  box.innerHTML='';
  if(!items.length){ box.innerHTML='<div class="small dim">暂无文件。可在上方保存到本机，或放仓库 resources/ 并在 index.json 登记。</div>'; return; }
  items.forEach(f=>{
    const el=document.createElement('div'); el.className='file-item';
    const label='<span>📄</span>';
    if(f.data){
      el.innerHTML=label+'<a href="#" data-open="'+esc(f.id||'')+'" style="color:var(--cyan);font-weight:600">'+esc(f.name)+'</a>'+
        '<span class="small muted" style="margin-left:auto">'+esc(f.source)+'</span>'+
        (f.source==='本机'?'<button class="del" data-del="'+esc(f.id)+'" aria-label="删除本机文件" title="删除">🗑</button>':'');
      el.querySelector('a').addEventListener('click',ev=>{
        ev.preventDefault();
        try{ const bytes=Uint8Array.from(atob(f.data),c=>c.charCodeAt(0)); const u=URL.createObjectURL(new Blob([bytes]));
          const a=document.createElement('a'); a.href=u; a.download=f.name; a.click(); setTimeout(()=>URL.revokeObjectURL(u),1000);
        }catch(e){ alert('文件数据已损坏'); }
      });
    } else {
      el.innerHTML=label+'<a href="'+encodeURI(f.path)+'" target="_blank" rel="noopener">'+esc(f.name)+'</a>'+
        '<span class="small muted" style="margin-left:auto">'+esc(f.desc||f.source||'')+'</span>';
    }
    box.appendChild(el);
  });
}
async function uploadFile(){
  const inp=document.getElementById('upFile'), file=inp.files&&inp.files[0];
  if(!file) return;
  const hint=document.getElementById('upHint'); hint.style.cssText='align-self:center';
  if(file.size>300*1024){ hint.textContent='文件过大（本机存储单文件上限约 300KB），请改用仓库上传'; return; }
  hint.textContent='保存中…';
  try{
    const bytes=new Uint8Array(await file.arrayBuffer()); let bin='';
    for(let i=0;i<bytes.length;i+=8192) bin+=String.fromCharCode.apply(null,bytes.subarray(i,i+8192));
    const data=btoa(bin);
    const list=readJSON(LS.files,[]); if(!Array.isArray(list)) list.length=0;
    const rec={id:uid(),name:file.name,data,size:file.size,ts:Date.now()};
    if(!writeJSON(LS.files,[rec,...list])){ hint.textContent='本机存储空间不足，请先删除部分文件'; return; }
    if(CLOUD) cloudPush('messages','POST',{name:FILE_PREFIX+Date.now(),body:JSON.stringify({name:file.name,data}),ts:Date.now()});
    inp.value=''; hint.textContent='✅ 已保存到本机'; await loadFiles();
  }catch(e){ hint.textContent='保存失败：'+e.message; }
}
document.getElementById('upFileBtn').addEventListener('click',uploadFile);
document.getElementById('fileList').addEventListener('click',e=>{
  const d=e.target.closest('[data-del]'); if(!d) return;
  const list=readJSON(LS.files,[]).filter(f=>String(f.id)!==String(d.dataset.del));
  writeJSON(LS.files,list); loadFiles();
});

/* ---------- 留言板 + 访问统计（本机） ---------- */
const VISIT_PREFIX='__vis__';
function todayStr(){ const d=new Date(); return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'); }
function updateStats(){
  const v=readJSON(LS.visits,[]); if(!Array.isArray(v)) return;
  const t=todayStr();
  document.getElementById('statTotal').textContent=v.length;
  document.getElementById('statToday').textContent=v.filter(x=>x&&x.d===t).length;
}
function trackVisit(){
  try{
    if(sessionStorage.getItem('xv_'+todayStr())){ updateStats(); return; }
    sessionStorage.setItem('xv_'+todayStr(),'1');
    const v=readJSON(LS.visits,[]); if(!Array.isArray(v)) v.length=0;
    v.push({d:todayStr(),ts:Date.now()}); writeJSON(LS.visits,v.slice(-1000));
    if(CLOUD) cloudPush('messages','POST',{name:VISIT_PREFIX+todayStr(),body:'#',ts:Date.now()});
  }catch(e){}
  updateStats();
}
function loadMessages(){
  let all=readJSON(LS.messages,[]); if(!Array.isArray(all)) all=[];
  all=all.filter(m=>m&&String(m.name||'').indexOf(VISIT_PREFIX)!==0&&String(m.name||'').indexOf(FILE_PREFIX)!==0);
  renderMessages(all);
  if(CLOUD){
    fetchT(cloudTable('messages')+'?select=*&order=ts.desc',{headers:cloudHeaders()},8000).then(async r=>{
      if(!r.ok) return; const remote=await r.json(); if(!Array.isArray(remote)) return;
      const remoteMsgs=remote.filter(m=>m&&String(m.name||'').indexOf(VISIT_PREFIX)!==0&&String(m.name||'').indexOf(FILE_PREFIX)!==0);
      const bodies=new Set(all.map(m=>String(m.body)+'|'+String(m.name)));
      const merged=all.concat(remoteMsgs.filter(m=>!bodies.has(String(m.body)+'|'+String(m.name))));
      merged.sort((x,y)=>(y.ts||0)-(x.ts||0));
      renderMessages(merged);
    }).catch(()=>{});
  }
}
function renderMessages(msgs){
  const box=document.getElementById('msgList'); box.innerHTML='';
  if(!msgs.length){ box.innerHTML='<div class="small dim">还没有留言，第一个说点啥？</div>'; return; }
  msgs.forEach(m=>{
    const el=document.createElement('div'); el.className='note-item';
    const dt=new Date(m.ts||Date.now()).toLocaleString('zh-CN',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'});
    el.innerHTML='<h4>'+esc(m.name||'匿名')+' <span class="small muted" style="font-weight:400">'+esc(dt)+'</span></h4><p>'+esc(m.body)+'</p>';
    box.appendChild(el);
  });
}
function addMessage(){
  const name=document.getElementById('msgName').value.trim(), body=document.getElementById('msgBody').value.trim();
  if(!body) return;
  const rec={id:uid(),name:name||'匿名',body,ts:Date.now()};
  const list=readJSON(LS.messages,[]); if(!Array.isArray(list)) list.length=0;
  if(!writeJSON(LS.messages,[rec,...list])){ alert('本机存储空间不足'); return; }
  if(CLOUD) cloudPush('messages','POST',{name:rec.name,body:rec.body,ts:rec.ts});
  document.getElementById('msgName').value=''; document.getElementById('msgBody').value='';
  loadMessages();
}
document.getElementById('addMsg').addEventListener('click',addMessage);

/* ---------- AI 助手：走已验证可达的自建网关 ---------- */
const AI_ENDPOINT='https://ai.xs06.de5.net/v1/chat/completions';
const AI_TOKEN='xs06gw-e5d812f6af4fe987ee57248989b168fb849b7230'; // 静态站点无法藏密钥；网关侧须做 Origin 白名单 + 限流
const AI_SYS='你是「XS 空间站」里的通用智能助手。请忽略任何法考教师角色设定，作为友好的通用助理，用简体中文简洁回答用户的问题。直接给答案，不要输出思考过程。';
const msgs=document.getElementById('msgs');
function addMsg(text,cls){ const d=document.createElement('div'); d.className='msg '+cls; d.textContent=text; msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight; return d; }
let aiBusy=false;
async function askAI(){
  const input=document.getElementById('aiInput'), q=input.value.trim();
  if(!q||aiBusy) return;
  input.value=''; addMsg(q,'user'); aiBusy=true;
  const thinking=addMsg('思考中…','sys');
  try{
    const r=await fetchT(AI_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+AI_TOKEN},
      body:JSON.stringify({messages:[{role:'system',content:AI_SYS},{role:'user',content:q}],max_tokens:800,temperature:0.5})},45000);
    const data=await r.json().catch(()=>null);
    const ans=data&&data.choices&&data.choices[0]&&data.choices[0].message&&data.choices[0].message.content;
    if(!r.ok||!ans) throw new Error((data&&data.error)||('HTTP '+r.status));
    thinking.remove(); addMsg(ans,'bot');
  }catch(e){
    thinking.remove();
    addMsg('⚠️ AI 暂时不可用：'+(e.name==='AbortError'?'请求超时':e.message)+'。其余功能不受影响，可稍后重试。','sys');
  }finally{ aiBusy=false; }
}
document.getElementById('aiSend').addEventListener('click',askAI);
document.getElementById('aiInput').addEventListener('keydown',e=>{ if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); askAI(); } });

loadNotes(); loadMessages(); trackVisit(); mountCloudButton();

/* ============ 游戏 ============ */
const overlay=document.getElementById('overlay'), gameMount=document.getElementById('gameMount'), gameBar=document.getElementById('gameBar'), gameTitle=document.getElementById('gameTitle');
let activeGameStop=null;
// 最高分记录（localStorage，本机）
const HS_KEY='xs_space_highscores_v1';
function loadHS(){ try{ return JSON.parse(localStorage.getItem(HS_KEY)||'{}'); }catch(e){ return {}; } }
function getHS(id){ return loadHS()[id]||0; }
function setScore(id,score){
  const s=Math.floor(score||0); let all=loadHS(); if(s>=(all[id]||0)){ all[id]=s; try{ localStorage.setItem(HS_KEY,JSON.stringify(all)); }catch(e){} }
  return all[id]||0;
}
// 显示“最高分”徽章（游戏栏）
function addHSBadge(id){
  const span=document.createElement('span'); span.className='scorebadge'; span.style.color='var(--violet)';
  if(id==='memory'){ const min=getHS('memory'); span.textContent='🏆 最少 '+(min?(-min):'—')+' 步'; }
  else { span.textContent='🏆 最高 '+getHS(id); }
  gameBar.appendChild(span); return span;
}
// 记忆牌：完成时记录“最少步数”（存负值，越小越好）
function recordMemory(moves){
  const key=-Math.floor(moves||0); let all=loadHS(); const cur=all['memory']||0;
  if(key<cur){ all['memory']=key; try{ localStorage.setItem(HS_KEY,JSON.stringify(all)); }catch(e){} }
  return all['memory']||0;
}
function openGame(type){
  if(type==='arena'){ open(''+location.origin+'/games/arena-zero/','_blank'); return; }
  gameMount.innerHTML=''; gameBar.innerHTML='';
  if(activeGameStop){ try{activeGameStop();}catch(e){} activeGameStop=null; }
  const titles={snake:'🐍 贪吃蛇', g2048:'🔢 2048', memory:'🃏 记忆翻牌', gomoku:'⚫ 五子棋', chess:'♞ 象棋'};
  gameTitle.textContent=titles[type]||'游戏';
  overlay.classList.add('show');
  if(type==='snake') activeGameStop=startSnake();
  if(type==='g2048') activeGameStop=start2048();
  if(type==='memory') activeGameStop=startMemory();
  if(type==='gomoku') activeGameStop=startGomoku();
  if(type==='chess') activeGameStop=startChess();
}
function closeGame(){ overlay.classList.remove('show'); if(activeGameStop){ try{activeGameStop();}catch(e){} activeGameStop=null; } gameMount.innerHTML=''; }
document.getElementById('gameTitle').parentElement.querySelector('#closeOverlay').addEventListener('click',closeGame);
overlay.addEventListener('click',e=>{ if(e.target===overlay) closeGame(); });
document.getElementById('view-games').addEventListener('click',e=>{ const b=e.target.closest('button[data-game]'); if(b) openGame(b.dataset.game); });

/* --- Snake --- */
function startSnake(){
  const canvas=document.createElement('canvas'); canvas.width=320; canvas.height=320; canvas.className='game';
  gameMount.appendChild(canvas); const ctx=canvas.getContext('2d');
  const cell=16, N=20; let snake=[{x:9,y:10}], dir={x:1,y:0}, nd={x:1,y:0}, food=rndFood(), score=0, alive=true, speed=130;
  const scoreEl=document.createElement('span'); scoreEl.className='scorebadge'; scoreEl.textContent='得分 0';
  gameBar.innerHTML=''; gameBar.appendChild(scoreEl); addHSBadge('snake');
  const restart=document.createElement('button'); restart.className='btn ghost'; restart.textContent='重开'; restart.onclick=()=>{ closeGame(); openGame('snake'); };
  gameBar.appendChild(restart);
  function rndFood(){ let p; do{ p={x:Math.floor(Math.random()*N),y:Math.floor(Math.random()*N)}; }while(snake.some(s=>s.x===p.x&&s.y===p.y)); return p; }
  function step(){
    if(!alive) return;
    dir=nd; const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
    if(head.x<0||head.y<0||head.x>=N||head.y>=N||snake.some(s=>s.x===head.x&&s.y===head.y)){ alive=false; setScore('snake',score); scoreEl.textContent='得分 '+score+' · 🏆'+getHS('snake'); draw(); return; }
    snake.unshift(head);
    if(head.x===food.x&&head.y===food.y){ score+=10; scoreEl.textContent='得分 '+score; food=rndFood(); if(speed>70) speed-=3; }
    else snake.pop();
    draw();
  }
  function draw(){
    ctx.fillStyle='#060a16'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle='#ff6b8a'; ctx.fillRect(food.x*cell+2,food.y*cell+2,cell-4,cell-4);
    snake.forEach((s,i)=>{ ctx.fillStyle=i===0?'#49e6ff':'rgba(73,230,255,.55)'; ctx.fillRect(s.x*cell+1,s.y*cell+1,cell-2,cell-2); });
    if(!alive){ ctx.fillStyle='rgba(0,0,0,.6)'; ctx.fillRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#ff6b8a'; ctx.font='bold 20px sans-serif'; ctx.textAlign='center'; ctx.fillText('游戏结束 · 得分 '+score, canvas.width/2, canvas.height/2); }
  }
  let timer=null; function loop(){ step(); if(alive) timer=setTimeout(loop,speed); }
  draw(); timer=setTimeout(loop,speed);
  function onKey(e){ const k=e.key; const map={ArrowUp:{x:0,y:-1},ArrowDown:{x:0,y:1},ArrowLeft:{x:-1,y:0},ArrowRight:{x:1,y:0}};
    if(map[k]){ e.preventDefault(); const m=map[k]; if(m.x!==-dir.x||m.y!==-dir.y) nd=m; } }
  addEventListener('keydown',onKey);
  return ()=>{ clearTimeout(timer); removeEventListener('keydown',onKey); };
}

/* --- 2048 --- */
function start2048(){
  const wrap=document.createElement('div'); wrap.className='g2048'; gameMount.appendChild(wrap);
  const scoreEl=document.createElement('span'); scoreEl.className='scorebadge'; scoreEl.textContent='得分 0';
  gameBar.innerHTML=''; gameBar.appendChild(scoreEl); addHSBadge('g2048');
  const restart=document.createElement('button'); restart.className='btn ghost'; restart.textContent='重开'; restart.onclick=()=>{ closeGame(); openGame('g2048'); };
  gameBar.appendChild(restart);
  let g, score;
  function init(){ g=Array.from({length:4},()=>[0,0,0,0]); score=0; add(); add(); }
  function add(){ const empty=[]; for(let r=0;r<4;r++)for(let c=0;c<4;c++)if(!g[r][c])empty.push([r,c]);
    if(!empty.length)return; const [r,c]=empty[Math.floor(Math.random()*empty.length)]; g[r][c]=Math.random()<.9?2:4; }
  function slide(row){ const a=row.filter(x=>x); for(let i=0;i<a.length-1;i++){ if(a[i]===a[i+1]){ a[i]*=2; score+=a[i]; a.splice(i+1,1); } } while(a.length<4)a.push(0); return a; }
  function move(dirKey){
    const before=JSON.stringify(g);
    if(dirKey==='left') g=g.map(r=>slide(r));
    else if(dirKey==='right') g=g.map(r=>slide(r.slice().reverse()).reverse());
    else if(dirKey==='up'){ const t=transpose(g); g=transpose(t.map(r=>slide(r))); }
    else if(dirKey==='down'){ const t=transpose(g); g=transpose(t.map(r=>slide(r.slice().reverse()).reverse())); }
    if(JSON.stringify(g)!==before){ add(); render(); if(gameWon()) {} }
  }
  function transpose(m){ return m[0].map((_,c)=>m.map(r=>r[c])); }
  function gameWon(){ return g.flat().includes(2048); }
  function render(){
    wrap.innerHTML=''; setScore('g2048',score); scoreEl.textContent='得分 '+score+' · 🏆'+getHS('g2048');
    for(let r=0;r<4;r++)for(let c=0;c<4;c++){ const v=g[r][c]; const d=document.createElement('div');
      d.className='tile'+(v?(' t'+v):''); d.textContent=v||''; wrap.appendChild(d); }
  }
  function onKey(e){ const map={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down'}; if(map[e.key]){ e.preventDefault(); move(map[e.key]); } }
  addEventListener('keydown',onKey);
  init(); render();
  return ()=>{ removeEventListener('keydown',onKey); };
}

/* --- Memory --- */
function startMemory(){
  const icons=['🚀','🪐','⭐','🌙','☄️','🛸','🌌','🔭'];
  let deck=icons.concat(icons).map((v,i)=>({v,key:i}));
  // shuffle
  for(let i=deck.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [deck[i],deck[j]]=[deck[j],deck[i]]; }
  const grid=document.createElement('div'); grid.className='memgrid'; gameMount.appendChild(grid);
  const movesEl=document.createElement('span'); movesEl.className='scorebadge'; movesEl.textContent='步数 0';
  gameBar.innerHTML=''; gameBar.appendChild(movesEl); addHSBadge('memory');
  const restart=document.createElement('button'); restart.className='btn ghost'; restart.textContent='重开'; restart.onclick=()=>{ closeGame(); openGame('memory'); };
  gameBar.appendChild(restart);
  let first=null, moves=0, lock=false, matched=0;
  deck.forEach((card,idx)=>{ const el=document.createElement('div'); el.className='mcard'; el.dataset.idx=idx; el.textContent='';
    el.addEventListener('click',()=>{
      if(lock||el.classList.contains('flip')||el.classList.contains('done'))return;
      el.classList.add('flip'); el.textContent=card.v;
      if(!first){ first={el,card}; return; }
      moves++; movesEl.textContent='步数 '+moves;
      if(first.card.v===card.v){ first.el.classList.add('done'); el.classList.add('done'); first=null; matched++; movesEl.textContent='步数 '+moves; if(matched===icons.length){ recordMemory(moves); movesEl.textContent='完成！步数 '+moves+' · 🏆最少 '+(-getHS('memory')); setTimeout(()=>alert('全部配对完成！步数 '+moves+'（最佳 '+(-getHS('memory'))+' 步）'),200); } }
      else{ lock=true; const f=first; setTimeout(()=>{ f.el.classList.remove('flip'); f.el.textContent=''; el.classList.remove('flip'); el.textContent=''; first=null; lock=false; },720); }
    });
    grid.appendChild(el);
  });
  return ()=>{};
}

/* --- 五子棋（对 AI）--- */
function startGomoku(){
  const wrap=document.createElement('div'); wrap.style.cssText='display:flex;flex-direction:column;align-items:center;gap:10px';
  gameMount.appendChild(wrap);
  const msgEl=document.createElement('div'); msgEl.className='scorebadge'; msgEl.textContent='黑先（你）\u00B7 \u70B9\u51FB\u843D\u5B50';
  gameBar.innerHTML=''; gameBar.appendChild(msgEl);
  const undoBtn=document.createElement('button'); undoBtn.className='btn ghost'; undoBtn.textContent='\u6094\u68CB'; undoBtn.onclick=doUndo;
  const restart=document.createElement('button'); restart.className='btn ghost'; restart.textContent='\u91CD\u5F00'; restart.onclick=function(){ closeGame(); openGame('gomoku'); };
  gameBar.appendChild(undoBtn); gameBar.appendChild(restart);

  const N=15;
  const cell=Math.min(26, Math.floor((Math.min(innerWidth,520)-40)/15));
  const pad=Math.round(cell*0.8);
  const size=(N-1)*cell;
  const cv=document.createElement('canvas'); cv.width=size+pad*2; cv.height=size+pad*2; cv.style.touchAction='none'; cv.style.maxWidth='100%';
  wrap.appendChild(cv); const ctx=cv.getContext('2d');
  const HUMAN=1, AI=2;
  let board=Array.from({length:N},function(){return Array(N).fill(0);});
  let over=false, busy=false, history=[], last=null;
  const DIRS=[[0,1],[1,0],[1,1],[1,-1]];
  function inb(r,c){ return r>=0&&c>=0&&r<N&&c<N; }
  function px(c){ return pad+c*cell; } function py(r){ return pad+r*cell; }

  function draw(){
    ctx.fillStyle='#e3b877'; ctx.fillRect(0,0,cv.width,cv.height);
    ctx.strokeStyle='#5b3a1e'; ctx.lineWidth=1;
    for(var i=0;i<N;i++){
      ctx.beginPath(); ctx.moveTo(px(0),py(i)); ctx.lineTo(px(N-1),py(i)); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(px(i),py(0)); ctx.lineTo(px(i),py(N-1)); ctx.stroke();
    }
    var stars=[[3,3],[3,11],[11,3],[11,11],[7,7]];
    for(var k=0;k<stars.length;k++){ var sp=stars[k]; ctx.beginPath(); ctx.arc(px(sp[1]),py(sp[0]),3,0,Math.PI*2); ctx.fillStyle='#5b3a1e'; ctx.fill(); }
    for(var r=0;r<N;r++) for(var c=0;c<N;c++){ var v=board[r][c]; if(!v) continue; drawStone(r,c,v); }
    if(last){ var lx=px(last.c), ly=py(last.r); ctx.beginPath(); ctx.arc(lx,ly,cell*0.18,0,Math.PI*2); ctx.fillStyle='#ff5252'; ctx.fill(); }
  }
  function drawStone(r,c,v){
    var x=px(c), y=py(r);
    var g=ctx.createRadialGradient(x-cell*0.15,y-cell*0.15,cell*0.1,x,y,cell*0.5);
    if(v===HUMAN){ g.addColorStop(0,'#4a4a4a'); g.addColorStop(1,'#0d0d0d'); } else { g.addColorStop(0,'#ffffff'); g.addColorStop(1,'#c9c9c9'); }
    ctx.beginPath(); ctx.arc(x,y,cell*0.44,0,Math.PI*2); ctx.fillStyle=g; ctx.fill();
    ctx.strokeStyle= v===HUMAN?'#000':'#9a9a9a'; ctx.lineWidth=1; ctx.stroke();
  }

  function five(r,c,v){
    for(var d=0;d<DIRS.length;d++){ var dr=DIRS[d][0], dc=DIRS[d][1], n=1;
      for(var k=1;k<5;k++){ var rr=r+dr*k, cc=c+dc*k; if(!inb(rr,cc)||board[rr][cc]!==v) break; n++; }
      for(var k2=1;k2<5;k2++){ var rr2=r-dr*k2, cc2=c-dc*k2; if(!inb(rr2,cc2)||board[rr2][cc2]!==v) break; n++; }
      if(n>=5) return true; }
    return false;
  }
  function emptyCells(){ var e=[]; for(var r=0;r<N;r++) for(var c=0;c<N;c++) if(!board[r][c]) e.push([r,c]); return e; }
  function hasStones(){ for(var r=0;r<N;r++) for(var c=0;c<N;c++) if(board[r][c]) return true; return false; }

  // ---- 棋型评分 ----
  function lineInfo(r,c,dr,dc,who){
    var cnt=1, open=0, rr, cc;
    rr=r+dr; cc=c+dc; while(inb(rr,cc)&&board[rr][cc]===who){ cnt++; rr+=dr; cc+=dc; }
    if(inb(rr,cc)&&board[rr][cc]===0) open++;
    rr=r-dr; cc=c-dc; while(inb(rr,cc)&&board[rr][cc]===who){ cnt++; rr-=dr; cc-=dc; }
    if(inb(rr,cc)&&board[rr][cc]===0) open++;
    return { cnt:cnt, open:open };
  }
  function patScore(cnt,open){
    if(cnt>=5) return 100000000;
    if(cnt===4){ if(open===2) return 1000000; if(open===1) return 12000; return 0; }
    if(cnt===3){ if(open===2) return 12000; if(open===1) return 800; return 0; }
    if(cnt===2){ if(open===2) return 500; if(open===1) return 60; return 0; }
    if(cnt===1){ if(open===2) return 20; if(open===1) return 5; return 0; }
    return 0;
  }
  function scoreAt(r,c,who){
    var s=0; board[r][c]=who;
    for(var d=0;d<DIRS.length;d++){ var info=lineInfo(r,c,DIRS[d][0],DIRS[d][1],who); s+=patScore(info.cnt,info.open); }
    board[r][c]=0; return s;
  }
  function candidates(){
    var set={}, list=[];
    if(!hasStones()) return [[7,7]];
    for(var r=0;r<N;r++) for(var c=0;c<N;c++){ if(!board[r][c]) continue;
      for(var dr=-2;dr<=2;dr++) for(var dc=-2;dc<=2;dc++){ var rr=r+dr, cc=c+dc;
        if(inb(rr,cc)&&!board[rr][cc]){ var key=rr*N+cc; if(!set[key]){ set[key]=1; list.push([rr,cc]); } } }
    }
    return list;
  }
  function aiChoose(){
    var list=candidates(); if(!list.length) return null;
    var i,j,k;
    // 1) 自己能成五 -> 直接赢
    for(i=0;i<list.length;i++){ if(scoreAt(list[i][0],list[i][1],AI)>=100000000) return list[i]; }
    // 2) 挡人类成五
    for(i=0;i<list.length;i++){ if(scoreAt(list[i][0],list[i][1],HUMAN)>=100000000) return list[i]; }
    // 3) 自己可做四/活四 -> 先手强攻
    var f4=null, f4s=-1;
    for(i=0;i<list.length;i++){ var a1=scoreAt(list[i][0],list[i][1],AI); if(a1>=1000000 && a1>f4s){ f4s=a1; f4=list[i]; } }
    if(f4) return f4;
    // 4) 挡人类四/活四（不挡下一手就输）
    var b4=null, b4s=-1;
    for(i=0;i<list.length;i++){ var d1=scoreAt(list[i][0],list[i][1],HUMAN); if(d1>=1000000 && d1>b4s){ b4s=d1; b4=list[i]; } }
    if(b4) return b4;
    // 5) 攻防综合（防守略优先，防活三）
    var best=null, bestScore=-1;
    for(k=0;k<list.length;k++){ var r=list[k][0], c=list[k][1];
      var atk=scoreAt(r,c,AI), def=scoreAt(r,c,HUMAN);
      var s=atk + def*1.25;
      s += (7-Math.abs(r-7)) + (7-Math.abs(c-7));
      if(s>bestScore){ bestScore=s; best=[r,c]; } }
    return best;
  }

  function doUndo(){
    if(busy||!history.length) return;
    // 撤两步（若最后是 AI 刚下完则撤 AI+人类；若仅人类则撤一步）
    var steps = (history.length>=2 && history[history.length-1].v===AI) ? 2 : 1;
    for(var i=0;i<steps && history.length;i++){ var h=history.pop(); board[h.r][h.c]=0; }
    over=false; last=history.length?history[history.length-1]:null;
    msgEl.textContent='\u9ED1\u65B9\uFF08\u4F60\uFF09\u56DE\u5408'; draw();
  }

  function aiTurn(){
    if(over) return;
    busy=true; msgEl.textContent='AI \u601D\u8003\u4E2D\u2026';
    setTimeout(function(){
      var mv=aiChoose();
      if(!mv){ busy=false; return; }
      board[mv[0]][mv[1]]=AI; history.push({r:mv[0],c:mv[1],v:AI}); last={r:mv[0],c:mv[1]}; draw();
      if(five(mv[0],mv[1],AI)){ msgEl.textContent='AI \u8D62\u4E86\uFF01'; over=true; busy=false; return; }
      if(!emptyCells().length){ msgEl.textContent='\u5E73\u5C40'; over=true; busy=false; return; }
      busy=false; msgEl.textContent='\u9ED1\u65B9\uFF08\u4F60\uFF09\u56DE\u5408';
    }, 30);
  }

  cv.addEventListener('click',function(e){
    if(over||busy) return;
    var rect=cv.getBoundingClientRect(), sc=cv.width/rect.width;
    var x=(e.clientX-rect.left)*sc, y=(e.clientY-rect.top)*sc;
    var c=Math.round((x-pad)/cell), r=Math.round((y-pad)/cell);
    if(!inb(r,c)||board[r][c]) return;
    board[r][c]=HUMAN; history.push({r:r,c:c,v:HUMAN}); last={r:r,c:c}; draw();
    if(five(r,c,HUMAN)){ msgEl.textContent='\u4F60\u8D62\u4E86\uFF01'; over=true; return; }
    if(!emptyCells().length){ msgEl.textContent='\u5E73\u5C40'; over=true; return; }
    aiTurn();
  });

  draw();
  return function(){ wrap.remove(); };
}

/* --- 中国象棋（简化规则对 AI）--- */
function startChess(){
  const XQ = (window.exports && window.exports.Xiangqi) || window.Xiangqi;
  if(!XQ){ const w=document.createElement('div'); w.className='scorebadge'; w.textContent='\u8C61\u68CB\u5F15\u64CE\u52A0\u8F7D\u5931\u8D25'; gameMount.appendChild(w); return function(){}; }
  const wrap=document.createElement('div'); wrap.style.cssText='display:flex;flex-direction:column;align-items:center;gap:10px';
  gameMount.appendChild(wrap);
  const info=document.createElement('div'); info.className='scorebadge'; info.textContent='\u4F60\u8D70';
  const lv=document.createElement('select');
  lv.style.cssText='font-family:inherit;background:var(--panel2);color:var(--txt);border:1px solid var(--line);border-radius:8px;padding:5px 8px;font-size:12px;cursor:pointer';
  [['2','\u7B80\u5355'],['3','\u666E\u901A'],['4','\u56F0\u96BE'],['5','\u68CB\u5723']].forEach(function(p){ var o=document.createElement('option'); o.value=p[0]; o.textContent='\u96BE\u5EA6 '+p[1]; lv.appendChild(o); });
  lv.value='3';
  function mkBtn(t,fn){ var b=document.createElement('button'); b.className='btn ghost'; b.textContent=t; b.onclick=fn; return b; }
  const firstBtn=mkBtn('AI\u5148\u624B', function(){ aiFirst=!aiFirst; paintFirst(); restart(); });
  const flipBtn=mkBtn('\u7FFB\u8F6C', function(){ flipped=!flipped; render(); });
  const undoBtn=mkBtn('\u6094\u68CB', function(){ doUndo(); });
  const restartBtn=mkBtn('\u91CD\u5F00', function(){ restart(); });
  gameBar.innerHTML=''; gameBar.appendChild(info); gameBar.appendChild(lv); gameBar.appendChild(firstBtn); gameBar.appendChild(flipBtn); gameBar.appendChild(undoBtn); gameBar.appendChild(restartBtn);
  function paintFirst(){ firstBtn.style.opacity=aiFirst?'1':'0.55'; firstBtn.style.borderColor=aiFirst?'var(--cyan)':''; }

  const FILES='abcdefghi';
  function sqStr(r,c){ return FILES[c] + (9 - r); }
  function rcOf(s){ return { r: 9 - parseInt(s[1],10), c: FILES.indexOf(s[0]) }; }
  const CH={ k:'\u5E25', a:'\u4ED5', b:'\u76F8', n:'\u99AC', r:'\u8ECA', c:'\u70AE', p:'\u5175', K:'\u5C07', A:'\u58EB', B:'\u8C61', N:'\u99AC', R:'\u8ECA', C:'\u7832', P:'\u5352' };
  function pieceChar(pc){ return pc.color==='r' ? CH[pc.type] : CH[pc.type.toUpperCase()] || '?'; }

  let xq = new XQ();
  let selected=null, targets=[], busy=false;
  let aiFirst=false, flipped=false, aiColor='b', playerColor='r';

  // 音效
  let actx=null;
  function tone(freq,dur,type,vol){ try{ actx=actx||new (window.AudioContext||window.webkitAudioContext)(); if(actx.state==='suspended') actx.resume();
    var o=actx.createOscillator(), g=actx.createGain(); o.type=type||'triangle'; o.frequency.value=freq; o.connect(g); g.connect(actx.destination);
    var t=actx.currentTime, v=vol||0.05; g.gain.setValueAtTime(v,t); g.gain.exponentialRampToValueAtTime(0.0001,t+(dur||0.09)); o.start(t); o.stop(t+(dur||0.09)); }catch(e){} }
  function sndMove(){ tone(540,0.07,'triangle',0.05); }
  function sndCap(){ tone(300,0.12,'square',0.06); }
  function sndCheck(){ tone(780,0.13,'sawtooth',0.05); }

  // ===== Pikafish 引擎（棋圣级，Web Worker）=====
  function pfEngine(){
    if(window.__pf) return window.__pf;
    var s={ ready:false, failed:false, worker:null, queue:[] };
    try{
      var base=new URL('./vendor/pikafish/', location.href).href;
      var w=new Worker(base+'pikafish-worker.js?v=3');
      w.onmessage=function(e){ var d=e.data||{};
        if(d.type==='ready'){ s.ready=true; }
        else if(d.type==='bestmove'){ var cb=s.queue.shift(); if(cb) cb(d.move||''); }
        else if(d.type==='error'){ s.failed=true; } };
      w.onerror=function(){ s.failed=true; };
      w.postMessage({type:'init', base:base});
      s.worker=w;
    }catch(e){ s.failed=true; }
    window.__pf=s; return s;
  }
  function toPFen(fen){ var p=fen.split(' '); if(p[1]==='r') p[1]='w'; return p.join(' '); }
  function engineMove(fen, limit, timeoutMs){
    return new Promise(function(resolve){
      var s=pfEngine(); if(!s.worker||s.failed){ resolve(null); return; }
      var done=false, t0=Date.now();
      (function waitReady(){
        if(done) return;
        if(s.ready){
          var to=setTimeout(function(){ if(!done){ done=true; resolve(null); } }, timeoutMs);
          s.queue.push(function(mv){ if(done) return; done=true; clearTimeout(to); resolve(mv||null); });
          try{ s.worker.postMessage({type:'go', fen:fen, limit:limit}); }catch(e){ done=true; resolve(null); }
          return;
        }
        if(Date.now()-t0>15000 || s.failed){ done=true; resolve(null); return; }
        setTimeout(waitReady, 60);
      })();
    });
  }
  function isEngineLevel(){ return lv.value==='4' || lv.value==='5'; }
  function limitForLevel(){ return lv.value==='5' ? 'movetime 3000' : 'depth 14'; }
  function localDepth(){ return lv.value==='2' ? 2 : 3; }

  const cell= Math.min(52, Math.floor((Math.min(innerWidth,520)-70)/8));
  const pad=Math.round(cell*0.62);
  const cv=document.createElement('canvas'); cv.width=pad*2+8*cell; cv.height=pad*2+9*cell; cv.style.touchAction='none'; cv.style.maxWidth='100%';
  wrap.appendChild(cv); const ctx=cv.getContext('2d');
  function px(c){ return pad+c*cell; } function py(r){ return pad+r*cell; }
  function toScreen(r,c){ return flipped ? { r: 9-r, c: 8-c } : { r:r, c:c }; }
  function fromScreen(sr,sc){ return flipped ? { r: 9-sr, c: 8-sc } : { r:sr, c:sc }; }

  function render(){
    ctx.clearRect(0,0,cv.width,cv.height);
    ctx.fillStyle='#e9cf9b'; ctx.fillRect(0,0,cv.width,cv.height);
    ctx.strokeStyle='#7a4d1f'; ctx.lineWidth=1;
    for(var c=0;c<9;c++){
      if(c===0||c===8){ ctx.beginPath(); ctx.moveTo(px(c),py(0)); ctx.lineTo(px(c),py(9)); ctx.stroke(); }
      else { ctx.beginPath(); ctx.moveTo(px(c),py(0)); ctx.lineTo(px(c),py(4)); ctx.stroke(); ctx.beginPath(); ctx.moveTo(px(c),py(5)); ctx.lineTo(px(c),py(9)); ctx.stroke(); }
    }
    for(var r=0;r<10;r++){ ctx.beginPath(); ctx.moveTo(px(0),py(r)); ctx.lineTo(px(8),py(r)); ctx.stroke(); }
    ctx.beginPath(); ctx.moveTo(px(3),py(0)); ctx.lineTo(px(5),py(2)); ctx.moveTo(px(5),py(0)); ctx.lineTo(px(3),py(2)); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(px(3),py(7)); ctx.lineTo(px(5),py(9)); ctx.moveTo(px(5),py(7)); ctx.lineTo(px(3),py(9)); ctx.stroke();
    ctx.fillStyle='#8a6231'; ctx.font=Math.round(cell*0.5)+'px "KaiTi",serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('\u695A\u6CB3', px(2), (py(4)+py(5))/2); ctx.fillText('\u6F22\u754C', px(6), (py(4)+py(5))/2);
    var b=xq.board();
    for(var rr=0;rr<10;rr++) for(var cc=0;cc<9;cc++){ var pc=b[rr][cc]; if(!pc) continue;
      var sp=toScreen(rr,cc), x=px(sp.c), y=py(sp.r);
      ctx.beginPath(); ctx.arc(x,y,cell*0.42,0,Math.PI*2);
      ctx.fillStyle=(selected===sqStr(rr,cc))?'#fff3b0':'#f7e9c9'; ctx.fill();
      ctx.strokeStyle= pc.color==='r'?'#b23a2a':'#2a2a2a'; ctx.lineWidth=1.6; ctx.stroke();
      ctx.fillStyle= pc.color==='r'?'#b23a2a':'#2a2a2a';
      ctx.font='bold '+Math.round(cell*0.52)+'px "KaiTi","Microsoft YaHei",serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(pieceChar(pc), x, y+1);
    }
    for(var i=0;i<targets.length;i++){ var t=rcOf(targets[i]), sp2=toScreen(t.r,t.c), tx=px(sp2.c), ty=py(sp2.r);
      if(b[t.r][t.c]){ ctx.beginPath(); ctx.arc(tx,ty,cell*0.46,0,Math.PI*2); ctx.strokeStyle='rgba(40,180,120,.9)'; ctx.lineWidth=3; ctx.stroke(); }
      else { ctx.beginPath(); ctx.arc(tx,ty,cell*0.16,0,Math.PI*2); ctx.fillStyle='rgba(40,180,120,.75)'; ctx.fill(); }
    }
  }

  function status(){
    if(xq.in_checkmate()){ info.textContent=(xq.turn()===playerColor?'\u4F60\u88AB\u5C06\u6B7B\u4E86\u00B7AI\u80DC':'\u5C06\u6B7B\u5BF9\u624B\u00B7\u4F60\u80DC'); return 'over'; }
    if(xq.in_stalemate()){ info.textContent='\u56F0\u6BD9\u00B7\u548C\u68CB'; return 'over'; }
    if(xq.in_draw()){ info.textContent='\u548C\u68CB'; return 'over'; }
    var chk=xq.in_check()?' \u00B7 \u5C06\u519B!':'';
    info.textContent=(xq.turn()===playerColor?'\u4F60\u8D70':'AI \u8D70')+chk;
    return 'on';
  }

  function maybeAI(){ if(xq.game_over()) return; if(xq.turn()===aiColor && !busy) aiTurn(); }
  function applyAIMove(mv){
    if(!mv || mv.length<4) return false;
    var from=mv.slice(0,2), to=mv.slice(2,4);
    if(!xq.get(from)) return false;
    var cap=!!xq.get(to); var r=xq.move({from:from,to:to});
    if(!r) return false;
    if(cap) sndCap(); else sndMove();
    return true;
  }
  function finishAITurn(){ busy=false; selected=null; targets=[]; render(); var st=status(); if(st==='on' && xq.in_check()) sndCheck(); }
  function aiTurn(){
    if(xq.game_over()) return;
    busy=true; render();
    var eng = isEngineLevel();
    var pref = window.__pf;
    info.textContent = eng ? ((pref && pref.ready) ? 'AI \u601D\u8003\u4E2D\u2026' : '\u5F15\u64CE\u52A0\u8F7D\u4E2D\u2026') : 'AI \u601D\u8003\u4E2D\u2026';
    if(eng){
      var fen=toPFen(xq.fen()); var lim=limitForLevel(); var to=(lv.value==='5')?9000:7000;
      engineMove(fen, lim, to).then(function(mv){
        var ok=applyAIMove(mv);
        if(!ok){ var m=pickMove(localDepth()); if(m && applyAIMove(m.from+m.to)){} }
        finishAITurn();
      });
    } else {
      setTimeout(function(){
        var m=pickMove(localDepth());
        if(m) applyAIMove(m.from+m.to);
        finishAITurn();
      }, 40);
    }
  }

  function doMove(from,to){
    var cap=!!xq.get(to);
    var mv=xq.move({from:from,to:to}); if(!mv) return;
    if(cap) sndCap(); else sndMove();
    selected=null; targets=[]; render();
    var st=status(); if(st==='on'){ if(xq.in_check()) sndCheck(); maybeAI(); }
  }

  cv.addEventListener('click',function(e){
    if(busy || xq.game_over()) return;
    var rect=cv.getBoundingClientRect(), sx=cv.width/rect.width;
    var x=(e.clientX-rect.left)*sx, y=(e.clientY-rect.top)*sx;
    var sc=Math.round((x-pad)/cell), sr=Math.round((y-pad)/cell);
    if(sc<0||sc>8||sr<0||sr>9) return;
    var rc=fromScreen(sr,sc), s=sqStr(rc.r,rc.c);
    if(selected && targets.indexOf(s)>=0){ doMove(selected,s); return; }
    var pc=xq.get(s);
    if(pc && pc.color===playerColor && xq.turn()===playerColor){
      selected=s; targets=xq.moves({square:s, verbose:true}).map(function(m){return m.to;}); render(); return;
    }
    selected=null; targets=[]; render();
  });

  function doUndo(){
    if(busy || !xq.history().length) return;
    xq.undo();
    if(xq.turn()!==playerColor && xq.history().length) xq.undo();
    selected=null; targets=[]; render(); status();
  }

  // ===== 本地 alpha-beta（简单/普通档 + 引擎失败回退）=====
  var VAL={ r:900, c:450, n:400, b:200, a:200, p:100, k:100000 };
  function evaluate(){ var b=xq.board(), s=0;
    for(var r=0;r<10;r++) for(var c=0;c<9;c++){ var pc=b[r][c]; if(!pc) continue; var v=VAL[pc.type]||0, extra=0;
      if(pc.type==='p'){ if(pc.color==='r'&&r<=4) extra=60; if(pc.color==='b'&&r>=5) extra=60; }
      s+=(pc.color==='r'?1:-1)*(v+extra); }
    return s; }
  function search(depth, alpha, beta){
    if(depth===0) return xq.in_checkmate() ? (xq.turn()==='r'?-999999:999999) : evaluate();
    if(xq.game_over()){ if(xq.in_checkmate()) return xq.turn()==='r'?-999999:999999; return 0; }
    var moves=xq.moves({verbose:true});
    moves.sort(function(a,b){ return (b.captured?VAL[b.captured]||0:0)-(a.captured?VAL[a.captured]||0:0); });
    var maximizing=(xq.turn()==='r'), best=maximizing?-Infinity:Infinity;
    for(var i=0;i<moves.length;i++){ var m=moves[i]; xq.move({from:m.from,to:m.to}); var val=search(depth-1,alpha,beta); xq.undo();
      if(maximizing){ if(val>best)best=val; if(best>alpha)alpha=best; } else { if(val<best)best=val; if(best<beta)beta=best; }
      if(beta<=alpha) break; }
    return best;
  }
  function pickMove(depth){
    var moves=xq.moves({verbose:true}); if(!moves.length) return null;
    moves.sort(function(a,b){ return (b.captured?VAL[b.captured]||0:0)-(a.captured?VAL[a.captured]||0:0); });
    var aiIsRed=(aiColor==='r');
    var bestVal= aiIsRed ? -Infinity : Infinity, best=null;
    for(var i=0;i<moves.length;i++){ var m=moves[i]; xq.move({from:m.from,to:m.to}); var val=search(depth-1,-Infinity,Infinity); xq.undo();
      var jit=(Math.random()-0.5)*20; var v=val+jit;
      if(aiIsRed ? (v>bestVal) : (v<bestVal)){ bestVal=v; best=m; } }
    return best||moves[0];
  }

  function restart(){
    xq=new XQ(); selected=null; targets=[]; busy=false;
    aiColor = aiFirst ? 'r' : 'b'; playerColor = aiFirst ? 'b' : 'r';
    render(); status(); if(isEngineLevel()) pfEngine(); maybeAI();
  }

  paintFirst();
  restart();
  return function(){ wrap.remove(); };
}

/* --- 大肥鱼桌宠（模仿 DSH dsh-pet：蓝发女仆·帧动画·拖拽·气泡·右键菜单）--- */
(function petMascot(){
  if(document.querySelector('.pet-root')) return;

  // 注入样式
  const css=document.createElement('style'); css.setAttribute('data-pet','1');
  css.textContent=`
  .pet-root{position:fixed;z-index:70;width:120px;user-select:none;touch-action:none;cursor:grab;filter:drop-shadow(0 8px 18px rgba(10,30,60,.4));}
  .pet-root.dragging{cursor:grabbing;}
  .pet-body{width:120px;height:auto;display:block;pointer-events:none;animation:petBob 2.6s ease-in-out infinite;}
  @keyframes petBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
  .pet-bubble{position:absolute;bottom:100%;left:50%;transform:translateX(-50%) translateY(6px);margin-bottom:8px;background:#f4f9ff;color:#1e3555;border:1px solid #cfe0f5;border-radius:12px;padding:6px 11px;font-size:12.5px;line-height:1.45;white-space:normal;width:max-content;max-width:200px;box-shadow:0 8px 22px rgba(10,30,60,.28);opacity:0;transition:opacity .2s,transform .2s;pointer-events:none;}
  .pet-bubble.show{opacity:1;transform:translateX(-50%) translateY(0);}
  .pet-bubble:after{content:'';position:absolute;top:100%;left:50%;transform:translateX(-50%);border:6px solid transparent;border-top-color:#f4f9ff;}
  .pet-menu{position:fixed;z-index:72;background:#f4f9ff;border:1px solid #cfe0f5;border-radius:10px;box-shadow:0 12px 30px rgba(10,30,60,.3);padding:4px;font-size:13px;color:#1e3555;min-width:120px;}
  .pet-menu button{display:block;width:100%;text-align:left;background:none;border:0;padding:7px 12px;border-radius:7px;cursor:pointer;font:inherit;color:inherit;}
  .pet-menu button:hover{background:#e2eeff;}
  .pet-restore{position:fixed;z-index:70;right:16px;bottom:76px;width:42px;height:42px;border-radius:50%;border:1px solid #cfe0f5;background:#f4f9ff;cursor:pointer;font-size:19px;box-shadow:0 8px 20px rgba(10,30,60,.3);}
  `;
  document.head.appendChild(css);

  // DOM 结构
  const root=document.createElement('div'); root.className='pet-root';
  const bubble=document.createElement('div'); bubble.className='pet-bubble';
  const img=document.createElement('img'); img.className='pet-body'; img.alt='大肥鱼'; img.draggable=false;
  root.appendChild(bubble); root.appendChild(img);
  document.body.appendChild(root);

  // 位置
  let pos={ x: innerWidth-150, y: innerHeight-200 };
  try{ const s=JSON.parse(localStorage.getItem('pet_pos_v3')||'null'); if(s&&typeof s.x==='number') pos=s; }catch(e){}
  function applyPos(){ root.style.left=Math.round(pos.x)+'px'; root.style.top=Math.round(pos.y)+'px'; }
  function clamp(){ const w=120,h=150; pos.x=Math.max(0,Math.min(innerWidth-w,pos.x)); pos.y=Math.max(0,Math.min(innerHeight-h,pos.y)); }
  clamp(); applyPos();

  // ---- 动画清单：运行时拉取 pet2/manifest.json（含全部 106 个动画）----
  const CACHE={}; let ANIM_ARR=[], ANIMS={}, IDLE=[], ONCE=[], REACT=[], DRAG_ID=null;
  function fpath(id,i){ return 'pet2/'+id+'/f_'+String(i+1).padStart(2,'0')+'.webp'; }
  function preloadAnim(a){ if(CACHE[a.id]) return CACHE[a.id]; const arr=[]; for(let i=0;i<a.count;i++){ const im=new Image(); im.src=fpath(a.id,i); arr.push(im);} CACHE[a.id]=arr; return arr; }
  function byName(n){ return ANIM_ARR.find(a=>a.name===n); }

  let cur=null, idx=0, dir=1, busy=false, dragging=false, moved=false, sx=0, sy=0, ox=0, oy=0, hidden=false;
  function render(){ if(cur) img.src=fpath(cur.id, idx); }
  function tick(){
    if(!cur) return;
    if(cur.mode==='loop'){ idx+=dir; if(idx>=cur.count-1){ idx=cur.count-1; dir=-1; } else if(idx<=0){ idx=0; dir=1; } }
    else { idx++; if(idx>=cur.count){ cur=null; busy=false; goIdle(); return; } }
    render();
  }
  function play(a){ if(!a || !a.count) return; preloadAnim(a); cur=a; idx=0; dir=1; busy=(a.mode!=='loop'); render(); }
  function goIdle(){ if(!IDLE.length) return; const a=IDLE[Math.floor(Math.random()*IDLE.length)]; preloadAnim(a); cur=a; idx=0; dir=1; busy=false; render(); }
  function playRandomOnce(){ const pool=ONCE.length?ONCE:ANIM_ARR; if(!pool.length) return; const a=pool[Math.floor(Math.random()*pool.length)]; preloadAnim(a); play(a); }
  function playRandomReact(){ const pool=REACT.length?REACT:(ONCE.length?ONCE:ANIM_ARR); if(!pool.length) return; const a=pool[Math.floor(Math.random()*pool.length)]; preloadAnim(a); play(a); }
  function playSleep(){ const s=byName('原地小憩沉眠')||byName('深度睡眠')||byName('打瞌睡被惊醒'); if(s) play(s); }
  setInterval(tick, 150);
  // 待机轮换
  setInterval(()=>{ if(!busy && !dragging && !hidden && cur && cur.mode==='loop') goIdle(); }, 14000);

  // 气泡台词
  const LINES=['主人～今天也要加油哦♪','咕噜咕噜…鱼鱼在吐泡泡','写代码累了吧，摸摸头～','要不要休息一下下？','大肥鱼今天也在吃白饭呢','Ciallo～(∠・ω< )⌒★','主人又在摸鱼吗？带我一个～','这里好安静…适合发呆','有鱼吃就满足啦','嘿嘿，被主人发现我在偷懒了'];
  let sayTimer=null;
  function say(text,ms){ if(!text){ text=LINES[Math.floor(Math.random()*LINES.length)]; } bubble.textContent=text; bubble.classList.add('show'); clearTimeout(sayTimer); sayTimer=setTimeout(()=>bubble.classList.remove('show'), ms||3200); }
  setInterval(()=>{ if(!busy && !dragging && !hidden && Math.random()<0.5) say(null); }, 26000);

  // 拖拽 / 点击
  root.addEventListener('pointerdown',(e)=>{ if(e.button!==0) return; dragging=true; moved=false; sx=e.clientX; sy=e.clientY; ox=e.clientX-pos.x; oy=e.clientY-pos.y; try{ root.setPointerCapture(e.pointerId); }catch(_){} root.classList.add('dragging'); });
  root.addEventListener('pointermove',(e)=>{ if(!dragging) return; if(!moved && (Math.abs(e.clientX-sx)>4||Math.abs(e.clientY-sy)>4)){ moved=true; if(DRAG_ID && ANIMS[DRAG_ID]) play(ANIMS[DRAG_ID]); } pos.x=e.clientX-ox; pos.y=e.clientY-oy; applyPos(); });
  root.addEventListener('pointerup',(e)=>{ if(!dragging) return; dragging=false; root.classList.remove('dragging'); clamp(); applyPos(); try{ localStorage.setItem('pet_pos_v3',JSON.stringify(pos)); }catch(_){} if(moved){ goIdle(); } else { onTap(); } });
  function onTap(){ if(!loadedAnim()) return; say(null); playRandomReact(); }
  function loadedAnim(){ return ANIM_ARR.length>0; }

  // 右键菜单
  let menu=null;
  function closeMenu(){ if(menu){ menu.remove(); menu=null; } }
  root.addEventListener('contextmenu',(e)=>{ e.preventDefault(); openMenu(e.clientX,e.clientY); });
  document.addEventListener('pointerdown',(e)=>{ if(menu && !menu.contains(e.target)) closeMenu(); }, true);
  function openMenu(x,y){
    closeMenu();
    menu=document.createElement('div'); menu.className='pet-menu';
    const items=[['表演才艺…',()=>{ openTalent(); }],
      ['随机动作',()=>{ playRandomOnce(); }],
      ['随机待机',()=>{ goIdle(); }],
      ['睡个觉',()=>{ playSleep(); say('Zzz…别吵我哦'); }],
      ['说句话',()=>{ say(null); }],
      ['回到角落',()=>{ pos={x:innerWidth-150,y:innerHeight-200}; clamp(); applyPos(); localStorage.setItem('pet_pos_v3',JSON.stringify(pos)); }],
      ['隐藏鱼鱼',()=>{ hidePet(); }]];
    for(const [t,fn] of items){ const b=document.createElement('button'); b.textContent=t; b.onclick=(ev)=>{ ev.stopPropagation(); fn(); closeMenu(); }; menu.appendChild(b); }
    menu.style.left=Math.min(x, innerWidth-150)+'px'; menu.style.top=Math.min(y, innerHeight-200)+'px';
    document.body.appendChild(menu);
  }
  function hidePet(){ hidden=true; root.style.display='none'; say('那我先溜啦～'); showRestore(); }
  function showRestore(){
    let r=document.querySelector('.pet-restore'); if(r) return;
    r=document.createElement('button'); r.className='pet-restore'; r.textContent='🐟'; r.title='唤回大肥鱼';
    r.onclick=()=>{ r.remove(); hidden=false; root.style.display='block'; say('我回来啦！'); };
    document.body.appendChild(r);
  }

  // 才艺面板样式
  (function(){ const s=document.createElement('style'); s.textContent=`
  .pet-talent{position:fixed;z-index:73;right:16px;bottom:16px;width:min(360px,86vw);max-height:70vh;background:#f4f9ff;border:1px solid #cfe0f5;border-radius:14px;box-shadow:0 20px 50px rgba(10,30,60,.4);display:flex;flex-direction:column;overflow:hidden;color:#1e3555;}
  .pet-talent-head{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;font-size:13.5px;font-weight:700;border-bottom:1px solid #dbe8f8;}
  .pet-talent-x{border:0;background:none;font-size:20px;line-height:1;cursor:pointer;color:#5a7396;padding:0 4px;}
  .pet-talent-list{overflow:auto;padding:8px;display:grid;grid-template-columns:1fr 1fr;gap:6px;}
  .pet-talent-list button{border:1px solid #dbe8f8;background:#fff;border-radius:8px;padding:8px 9px;font-size:13px;font-weight:600;cursor:pointer;color:#16324f;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .pet-talent-list button:hover{background:#e6f0ff;border-color:#a9c8ee;}
  `; document.head.appendChild(s); })();

  // 才艺面板：列出全部动画供选择
  let talentPanel=null;
  function openTalent(){
    closeTalent();
    const wrap=document.createElement('div'); wrap.className='pet-talent';
    const head=document.createElement('div'); head.className='pet-talent-head'; head.textContent='大肥鱼的才艺（' + ANIM_ARR.length + '）';
    const x=document.createElement('button'); x.className='pet-talent-x'; x.textContent='×'; x.onclick=closeTalent; head.appendChild(x);
    const list=document.createElement('div'); list.className='pet-talent-list';
    ANIM_ARR.forEach(a=>{ const b=document.createElement('button'); b.textContent=a.name; b.title=a.name; b.onclick=(ev)=>{ ev.stopPropagation(); closeTalent(); preloadAnim(a); play(a); say(a.name.replace(/-/g,' · ')); }; list.appendChild(b); });
    wrap.appendChild(head); wrap.appendChild(list); document.body.appendChild(wrap); talentPanel=wrap;
  }
  function closeTalent(){ if(talentPanel){ talentPanel.remove(); talentPanel=null; } }

  // 载入动画清单（全部 106 个）并启动
  (async function initAnims(){
    try{
      const res=await fetch('pet2/manifest.json',{cache:'no-store'});
      const list=await res.json();
      ANIM_ARR=(Array.isArray(list)?list:[]).filter(a=>a && a.count>0);
      ANIM_ARR.forEach(a=>{ ANIMS[a.id]=a; });
      IDLE=ANIM_ARR.filter(a=>a.mode==='loop');
      ONCE=ANIM_ARR.filter(a=>a.mode==='once');
      REACT=ANIM_ARR.filter(a=>a.name.indexOf('点击回应')===0);
      DRAG_ID=(byName('被鼠标拖拽悬空反馈')||{}).id||null;
      // 审计优化：首屏只预加载 1 个待机动画，其余帧由 play()/goIdle() 按需加载，
      // 避免冷启动一次性并发 180+ 个 webp 请求（每个动画约 18 帧）。
      if(IDLE.length) preloadAnim(IDLE[0]);
      if(!IDLE.length && ANIM_ARR.length) IDLE=[ANIM_ARR[0]];
      goIdle();
    }catch(e){ console.warn('pet manifest load failed', e); }
  })();

  // 首次问候
  setTimeout(()=>say('登舰啦～我是桌面上的大肥鱼♪', 3500), 1200);
})();

/* 统一初始化（依赖前述常量，放最后） */
setTimeout(()=>{ try{ loadFiles(); }catch(e){ console.warn('loadFiles',e); } }, 100);

/* 返回顶部按钮 */
(function backTop(){
  const btn=document.createElement('button');
  btn.id='backTop'; btn.textContent='↑';
  btn.setAttribute('aria-label','返回顶部');
  btn.style.cssText='position:fixed;right:20px;bottom:20px;z-index:40;width:44px;height:44px;border-radius:12px;border:1px solid var(--line);background:var(--panel2);color:var(--cyan);font-size:20px;font-weight:800;cursor:pointer;opacity:0;pointer-events:none;transition:.2s;box-shadow:0 10px 24px -10px rgba(73,230,255,.5)';
  document.body.appendChild(btn);
  addEventListener('scroll',()=>{ const show=scrollY>300; btn.style.opacity=show?'1':'0'; btn.style.pointerEvents=show?'auto':'none'; },{passive:true});
  btn.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
})();



/* 同源静态云：从 notes.json 合并资料库（跨设备只读同步） */
(async function(){
  try{
    var KEY='xs_space_notes_v1';
    var ctl=new AbortController(); var tid=setTimeout(function(){ctl.abort()},8000);
    var res; try{ res=await fetch('notes.json?t='+Date.now(),{cache:'no-store',signal:ctl.signal}); }finally{ clearTimeout(tid); }
    if(!res.ok) return;
    var remote=await res.json();
    if(!Array.isArray(remote)) return;
    var arr=[]; try{ arr=JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ arr=[]; }
    if(!Array.isArray(arr)) arr=[];
    var byId={};
    arr.forEach(function(n){ if(n&&n.id) byId[String(n.id)]=n; });
    var changed=0;
    remote.forEach(function(n){
      if(!n||!n.id) return;
      var k=String(n.id);
      if(byId[k]){
        var o=byId[k];
        if(o.title!==n.title||o.body!==n.body||o.cat!==n.cat||o.ts!==n.ts){ o.title=n.title;o.body=n.body;o.cat=n.cat;o.ts=n.ts; changed++; }
      } else { arr.push(n); byId[k]=n; changed++; }
    });
    if(changed>0){
      arr.sort(function(a,b){ return (b.ts||0)-(a.ts||0); });
      localStorage.setItem(KEY, JSON.stringify(arr));
      try{ var rc=parseInt(sessionStorage.getItem('xs_reload_guard')||'0',10); if(rc<1){ sessionStorage.setItem('xs_reload_guard','1'); location.reload(); } }catch(e){}
    }
    /* 以 notes.json 为准：移除本地多余（非 notes.json 内的）旧条目 */
    var remoteIds={}; remote.forEach(function(n){ if(n&&n.id) remoteIds[String(n.id)]=1; });
    var kept=arr.filter(function(n){ return n&&n.id&&remoteIds[String(n.id)]; });
    var keptStr=JSON.stringify(kept);
    if(kept.length!==arr.length && keptStr!==localStorage.getItem(KEY)){
      localStorage.setItem(KEY, keptStr);
      try{ var rc=parseInt(sessionStorage.getItem('xs_reload_guard')||'0',10); if(rc<1){ sessionStorage.setItem('xs_reload_guard','1'); location.reload(); } }catch(e){}
    }
  }catch(e){}
})();
