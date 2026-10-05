import io
import base64
import math
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = r'''
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ChemProcess Studio · Process Engineering Workspace</title>
<style>
:root{--ink:#f2f2f0;--muted:#a6a6a3;--dim:#70716f;--bg:#080808;--panel:#151515;--panel2:#222222;--line:rgba(220,220,216,.18);--teal:#d8d8d3;--blue:#3a3329;--coral:#d85c52;--yellow:#d99a2b;--shadow:0 24px 70px rgba(0,0,0,.42)}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 78% -10%,rgba(217,154,43,.12) 0,transparent 28%),radial-gradient(circle at 12% 30%,rgba(255,255,255,.06) 0,transparent 30%),var(--bg);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.4}button,input,select{font:inherit}button{cursor:pointer}.shell{display:flex;min-height:100vh}.sidebar{width:248px;border-right:1px solid var(--line);background:rgba(18,18,18,.72);backdrop-filter:blur(18px);padding:26px 16px;display:flex;flex-direction:column;position:sticky;top:0;height:100vh}.brand{display:flex;align-items:center;gap:11px;padding:0 12px 32px}.brand-mark{width:35px;height:35px;border:1px solid rgba(84,224,193,.55);border-radius:11px;display:grid;place-items:center;color:var(--teal);background:linear-gradient(145deg,rgba(255,255,255,.16),rgba(255,255,255,.03));font-weight:800;font-size:17px}.brand strong{font-size:14px;letter-spacing:.02em}.brand span{display:block;color:var(--muted);font-size:10px;margin-top:1px;letter-spacing:.08em;text-transform:uppercase}.nav-label{color:#566982;font-size:10px;letter-spacing:.14em;text-transform:uppercase;padding:0 12px 10px}.nav{display:grid;gap:6px}.nav button{border:1px solid transparent;background:transparent;color:var(--muted);padding:12px;border-radius:10px;text-align:left;display:flex;gap:11px;align-items:center;font-size:13px}.nav button:hover{background:rgba(255,255,255,.07);color:var(--ink)}.nav button.active{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.28);color:var(--ink)}.nav .icon{width:20px;text-align:center;font-size:16px}.side-note{margin-top:auto;background:#0d1b2d;border:1px solid var(--line);border-radius:12px;padding:14px;color:var(--muted);font-size:11px}.side-note b{display:block;color:var(--ink);font-size:12px;margin-bottom:6px}.main{flex:1;min-width:0;padding:30px 42px 48px}.topbar{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:30px}.eyebrow{color:var(--yellow);font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700}.topbar h1{font-size:30px;letter-spacing:-.045em;margin:5px 0 0}.topbar p{color:var(--muted);font-size:13px;margin:7px 0 0}.status{display:flex;align-items:center;gap:8px;color:var(--muted);font-size:12px;white-space:nowrap}.dot{width:8px;height:8px;border-radius:50%;background:var(--teal);box-shadow:0 0 0 4px rgba(84,224,193,.1)}.overview{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:26px}.stat{background:linear-gradient(135deg,rgba(38,38,38,.76),rgba(16,16,16,.78));backdrop-filter:blur(18px);border:1px solid var(--line);border-radius:14px;padding:17px 18px;position:relative;overflow:hidden}.stat:after{content:"";position:absolute;width:110px;height:110px;right:-40px;top:-50px;border:1px solid rgba(84,224,193,.16);border-radius:50%}.stat-label{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.1em}.stat-value{font-size:23px;font-weight:700;margin:5px 0 1px}.stat-sub{font-size:11px;color:var(--dim)}.workspace{background:rgba(24,24,24,.64);backdrop-filter:blur(22px);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);overflow:hidden}.workspace-head{padding:21px 24px 17px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:20px}.workspace-head h2{font-size:15px;margin:0;letter-spacing:-.02em}.workspace-head p{display:none}.module{padding:26px;display:none}.module.active{display:block}.module-intro{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;margin-bottom:15px}.module-title{display:flex;gap:13px}.module-icon{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;font-size:19px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.24);color:var(--ink)}.module h3{margin:0;font-size:16px}.module-copy{display:none}.tag{color:var(--yellow);border:1px solid rgba(217,154,43,.42);background:rgba(217,154,43,.09);font-size:10px;text-transform:uppercase;letter-spacing:.12em;padding:6px 9px;border-radius:100px;white-space:nowrap}.form-layout{display:grid;grid-template-columns:minmax(0,1fr) 270px;gap:25px}.fields{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:15px}.field label{display:flex;justify-content:space-between;gap:10px;color:#aebbd0;font-size:11px;margin:0 0 7px}.hint{color:var(--dim);font-size:10px}.field input,.field select{width:100%;border:1px solid rgba(58,51,41,.72);border-radius:9px;background:rgba(255,255,255,.055);color:var(--ink);padding:11px 12px;outline:none;transition:border .18s,box-shadow .18s}.field input:focus,.field select:focus{border-color:var(--yellow);box-shadow:0 0 0 3px rgba(217,154,43,.18)}.field.full{grid-column:1/-1}.field input[readonly]{color:#93a5bd;background:rgba(255,255,255,.06)}.actions{margin-top:20px;display:flex;gap:10px}.primary{border:0;border-radius:9px;padding:12px 17px;background:var(--yellow);color:#17130a;font-size:12px;font-weight:800;box-shadow:0 9px 22px rgba(217,154,43,.20)}.primary:hover{filter:brightness(1.06);transform:translateY(-1px)}.secondary{border:1px solid var(--line);border-radius:9px;padding:11px 15px;background:transparent;color:var(--muted);font-size:12px}.helper{border:1px solid var(--line);border-radius:13px;padding:16px;background:rgba(8,17,31,.54);height:max-content}.helper h4{font-size:12px;margin:0 0 14px}.helper-row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(32,50,74,.7);font-size:11px}.helper-row:last-child{border-bottom:0}.helper-row span{color:var(--muted)}.helper-row b{color:var(--ink);font-weight:600}.result{display:none;margin-top:24px;border:1px solid rgba(84,224,193,.25);border-radius:13px;background:linear-gradient(135deg,rgba(84,224,193,.08),rgba(10,22,39,.5));padding:18px}.result.visible{display:block}.result-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.result-head strong{font-size:12px}.result-head span{font-size:10px;color:var(--teal);text-transform:uppercase;letter-spacing:.12em}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.metric{background:rgba(5,15,28,.42);border:1px solid rgba(32,50,74,.8);border-radius:9px;padding:12px}.metric span{display:block;color:var(--muted);font-size:10px;margin-bottom:5px}.metric b{font-size:16px}.plot{display:none;margin-top:16px;padding:10px;border-radius:10px;background:#091321;border:1px solid var(--line)}.plot.visible{display:block}.plot img{width:100%;display:block;border-radius:6px}.error{display:none;margin-top:14px;color:#f09b94;font-size:12px;background:rgba(255,125,117,.08);border:1px solid rgba(255,125,117,.3);padding:10px;border-radius:8px}.error.visible{display:block}.footer{color:#52647d;font-size:11px;text-align:center;margin-top:18px}.mobile-nav{display:none}
@media(max-width:900px){.sidebar{width:210px}.main{padding:25px}.form-layout{grid-template-columns:1fr}.helper{display:none}}
@media(max-width:650px){.overview{display:none}.shell{display:block}.sidebar{display:none}.main{padding:20px 14px 35px}.topbar{align-items:flex-start;margin-bottom:22px}.topbar h1{font-size:25px}.status{display:none}.stat{padding:13px 12px}.stat-value{font-size:17px}.stat-sub{font-size:9px}.workspace-head{padding:17px}.module{padding:16px 15px}.module-intro{display:block;margin-bottom:12px}.tag{display:inline-block;margin-top:8px;font-size:9px}.fields{grid-template-columns:1fr}.field.full{grid-column:auto}.actions{display:grid}.primary,.secondary{width:100%}.metrics{grid-template-columns:1fr 1fr}.metric:last-child{grid-column:1/-1}.mobile-nav{display:flex;position:sticky;top:0;z-index:5;background:rgba(8,17,31,.9);backdrop-filter:blur(14px);border-bottom:1px solid var(--line);padding:9px;gap:6px;overflow:auto}.mobile-nav button{flex:1;min-width:100px;background:transparent;border:1px solid transparent;color:var(--muted);padding:9px 8px;border-radius:8px;font-size:10px;white-space:nowrap}.mobile-nav button.active{color:var(--teal);background:rgba(84,224,193,.1);border-color:rgba(84,224,193,.2)}}
</style>
</head>
<body>
<div class="shell">
<aside class="sidebar"><div class="brand"><div class="brand-mark">∿</div><div><strong>ChemProcess</strong><span>Studio / v2.0</span></div></div><div class="nav-label">Workspaces</div><nav class="nav"><button class="active" data-tab="heat"><span class="icon">◈</span>Heat exchanger</button><button data-tab="fluid"><span class="icon">⌁</span>Pipe hydraulics</button><button data-tab="cre"><span class="icon">⌬</span>Reactor kinetics</button><button data-tab="distil"><span class="icon">◬</span>Distillation</button></nav><div class="side-note"><b>Engineering note</b>All results use deterministic first-principles models. Validate final designs against plant standards and operating constraints.</div></aside>
<main class="main"><nav class="mobile-nav"><button class="active" data-tab="heat">Exchanger</button><button data-tab="fluid">Hydraulics</button><button data-tab="cre">Reactor</button><button data-tab="distil">Distillation</button></nav>
<header class="topbar"><div><div class="eyebrow">Process engineering workspace</div><h1>Design with confidence.</h1><p>Fast, transparent calculations for thermal, fluid, reaction and separation systems.</p></div><div class="status"><i class="dot"></i>Calculation engine ready</div></header>
<section class="overview"><div class="stat"><div class="stat-label">Active modules</div><div class="stat-value">04</div><div class="stat-sub">Thermal · fluid · CRE · mass</div></div><div class="stat"><div class="stat-label">Exchanger</div><div class="stat-value">1-2 STHE</div><div class="stat-sub">Ft factor enabled</div></div><div class="stat"><div class="stat-label">Hydraulics</div><div class="stat-value">Pump TDH</div><div class="stat-sub">Brake HP sizing</div></div><div class="stat"><div class="stat-label">Distillation</div><div class="stat-value">Trays</div><div class="stat-sub">McCabe-Thiele stepping</div></div></section>
<section class="workspace"><div class="workspace-head"><div><h2 id="workspace-title">Heat exchanger rating</h2><p id="workspace-sub">Counter-flow energy balance, LMTD and required area.</p></div><span class="tag">Solver online</span></div>

<!-- 1. HEAT EXCHANGER -->
<div id="module-heat" class="module active"><div class="module-intro"><div class="module-title"><div class="module-icon">◈</div><div><h3>Heat Exchanger Rating (Counter & 1-2 STHE)</h3><p class="module-copy">Size required area from hot-side duty, cooling water balance, and flow geometry.</p></div></div><span class="tag">Thermal model</span></div><div class="form-layout"><div><div class="fields"><div class="field"><label>Exchanger geometry <span class="hint">pass arrangement</span></label><select id="hx_type"><option value="counter">Pure counter-flow (Ft = 1.0)</option><option value="1-2">1 Shell pass, 2+ Tube passes (1-2 STHE)</option></select></div><div class="field"><label>Hot process fluid <span class="hint">preset Cp</span></label><select id="hx_fluid_hot" onchange="updateHotPreset()"><option value="2.45">Hydrocarbon / Kerosene</option><option value="4.18">Water / Condensate</option><option value="2.05">Engine / Thermal oil</option><option value="2.57">Ethanol</option><option value="2.22">Gasoline</option><option value="custom">Custom fluid</option></select></div><div class="field"><label>Hot specific heat Cp<sub>h</sub> <span class="hint">kJ/kg·K</span></label><input id="hx_cph" type="number" step="any" value="2.45" readonly></div><div class="field"><label>Exchanger service <span class="hint">preset U</span></label><select id="hx_service" onchange="updateUPreset()"><option value="650">Liquid-liquid shell & tube</option><option value="1000">Water-to-water cooler</option><option value="450">Heavy organics / oil to water</option><option value="1800">Steam condenser</option><option value="120">Gas / air stream cooler</option><option value="custom">Custom coefficient</option></select></div><div class="field"><label>Overall U <span class="hint">W/m²·K</span></label><input id="hx_u" type="number" step="any" value="650" readonly></div><div class="field"><label>Hot flow rate m<sub>h</sub> <span class="hint">kg/s</span></label><input id="hx_mh" type="number" step="any" value="2.0"></div><div class="field"><label>Cold water flow m<sub>c</sub> <span class="hint">kg/s</span></label><input id="hx_mc" type="number" step="any" value="3.5"></div><div class="field"><label>Hot inlet T<sub>h,in</sub> <span class="hint">°C</span></label><input id="hx_thin" type="number" step="any" value="120"></div><div class="field"><label>Hot target outlet T<sub>h,out</sub> <span class="hint">°C</span></label><input id="hx_thout" type="number" step="any" value="65"></div><div class="field full"><label>Cooling water supply T<sub>c,in</sub> <span class="hint">°C</span></label><input id="hx_tcin" type="number" step="any" value="25"></div></div><div class="actions"><button class="primary" onclick="calculateHeat()">Run thermal sizing ↗</button><button class="secondary" onclick="resetModule('heat')">Reset inputs</button></div><div id="hx_error" class="error"></div><div id="hx_result" class="result"><div class="result-head"><strong>Energy balance & rating</strong><span>Calculated output</span></div><div id="hx_metrics" class="metrics"></div><div id="hx_plot" class="plot"><img id="hx_img"></div></div></div><div class="helper"><h4>Model reference</h4><div class="helper-row"><span>Duty</span><b>Q = m·Cp·ΔT</b></div><div class="helper-row"><span>Effective ΔT</span><b>Ft · LMTD</b></div><div class="helper-row"><span>Area</span><b>A = Q / (U·ΔT_eff)</b></div><div class="helper-row"><span>Cold side Cp</span><b>4.18 kJ/kg·K</b></div></div></div></div>

<!-- 2. HYDRAULICS -->
<div id="module-fluid" class="module"><div class="module-intro"><div class="module-title"><div class="module-icon">⌁</div><div><h3>Pipe Hydraulics & Pump Motor Sizing</h3><p class="module-copy">Evaluate velocity, friction loss, Total Dynamic Head (TDH), and pump motor horsepower.</p></div></div><span class="tag">Fluid model</span></div><div class="form-layout"><div><div class="fields"><div class="field"><label>Inner diameter D <span class="hint">m</span></label><input id="fl_d" type="number" step="any" value="0.05"></div><div class="field"><label>Pipe length L <span class="hint">m</span></label><input id="fl_l" type="number" step="any" value="100"></div><div class="field"><label>Volumetric flow Q <span class="hint">m³/h</span></label><input id="fl_q" type="number" step="any" value="10.0"></div><div class="field"><label>Fluid density ρ <span class="hint">kg/m³</span></label><input id="fl_rho" type="number" step="any" value="1000"></div><div class="field"><label>Dynamic viscosity μ <span class="hint">Pa·s</span></label><input id="fl_mu" type="number" step="any" value="0.001"></div><div class="field"><label>Pipe roughness ε <span class="hint">mm</span></label><input id="fl_roughness" type="number" step="any" value="0.045"></div><div class="field"><label>Static elevation lift Δz <span class="hint">m</span></label><input id="fl_dz" type="number" step="any" value="15.0"></div><div class="field"><label>Minor loss sum ΣK <span class="hint">fittings/valves</span></label><input id="fl_kminor" type="number" step="any" value="5.5"></div><div class="field full"><label>Pump efficiency η <span class="hint">fraction (0.4 - 0.9)</span></label><input id="fl_eta" type="number" step="any" value="0.70"></div></div><div class="actions"><button class="primary" onclick="calculateFluid()">Run hydraulic analysis ↗</button><button class="secondary" onclick="resetModule('fluid')">Reset inputs</button></div><div id="fl_error" class="error"></div><div id="fl_result" class="result"><div class="result-head"><strong>Hydraulics & pump sizing</strong><span>Calculated output</span></div><div id="fl_metrics" class="metrics"></div><div id="fl_plot" class="plot"><img id="fl_img"></div></div></div><div class="helper"><h4>Model reference</h4><div class="helper-row"><span>Velocity</span><b>Q / pipe area</b></div><div class="helper-row"><span>Regime</span><b>Reynolds number</b></div><div class="helper-row"><span>Total Head</span><b>TDH = Δz + hf + hm</b></div><div class="helper-row"><span>Brake Power</span><b>P = ρ·g·Q·TDH / η</b></div></div></div></div>

<!-- 3. CRE -->
<div id="module-cre" class="module"><div class="module-intro"><div class="module-title"><div class="module-icon">⌬</div><div><h3>Continuous Reactor Sizing (CSTR vs PFR)</h3><p class="module-copy">Estimate residence time, volume expansion ratio, and follow reactant decay.</p></div></div><span class="tag">Reaction model</span></div><div class="form-layout"><div><div class="fields"><div class="field"><label>Reaction order n <span class="hint">kinetic form</span></label><select id="cre_order"><option value="1">1st order · −rA = k·CA</option><option value="2">2nd order · −rA = k·CA²</option><option value="0">0 order · −rA = k</option></select></div><div class="field"><label>Feed flow rate v₀ <span class="hint">m³/h</span></label><input id="cre_v0" type="number" step="any" value="5.0"></div><div class="field"><label>Initial concentration C<sub>A0</sub> <span class="hint">mol/L</span></label><input id="cre_ca0" type="number" step="any" value="2.5"></div><div class="field"><label>Rate constant k <span class="hint">SI units</span></label><input id="cre_k" type="number" step="any" value="0.04"></div><div class="field full"><label>Target conversion X<sub>A</sub> <span class="hint">0 to 0.99</span></label><input id="cre_xa" type="number" step="any" value="0.85"></div></div><div class="actions"><button class="primary" onclick="calculateCRE()">Run reactor sizing ↗</button><button class="secondary" onclick="resetModule('cre')">Reset inputs</button></div><div id="cre_error" class="error"></div><div id="cre_result" class="result"><div class="result-head"><strong>Reactor sizing & kinetics</strong><span>Calculated output</span></div><div id="cre_metrics" class="metrics"></div><div id="cre_plot" class="plot"><img id="cre_img"></div></div></div><div class="helper"><h4>Model reference</h4><div class="helper-row"><span>CSTR Volume</span><b>V = v0·(CA0 - CA)/(-rA)</b></div><div class="helper-row"><span>PFR Volume</span><b>V = v0·∫ dX/(-rA)</b></div><div class="helper-row"><span>Ratio</span><b>V_CSTR / V_PFR</b></div><div class="helper-row"><span>Valid range</span><b>0 &lt; X &lt; 0.99</b></div></div></div></div>

<!-- 4. DISTILLATION -->
<div id="module-distil" class="module"><div class="module-intro"><div class="module-title"><div class="module-icon">◬</div><div><h3>McCabe-Thiele Binary Distillation</h3><p class="module-copy">Determine theoretical equilibrium stages, minimum reflux, and optimal feed tray.</p></div></div><span class="tag">Mass transfer</span></div><div class="form-layout"><div><div class="fields"><div class="field"><label>Feed mole fraction z<sub>F</sub> <span class="hint">0.05–0.95</span></label><input id="mc_zf" type="number" step="any" value="0.45"></div><div class="field"><label>Distillate purity x<sub>D</sub> <span class="hint">0.80–0.99</span></label><input id="mc_xd" type="number" step="any" value="0.95"></div><div class="field"><label>Bottoms purity x<sub>B</sub> <span class="hint">0.01–0.20</span></label><input id="mc_xb" type="number" step="any" value="0.05"></div><div class="field"><label>Relative volatility α <span class="hint">&gt; 1.1</span></label><input id="mc_alpha" type="number" step="any" value="2.40"></div><div class="field"><label>Feed thermal quality q <span class="hint">1 = sat. liquid</span></label><input id="mc_q" type="number" step="any" value="1.0"></div><div class="field"><label>Reflux multiplier <span class="hint">R / Rmin</span></label><input id="mc_rmult" type="number" step="any" value="1.30"></div></div><div class="actions"><button class="primary" onclick="calculateDistil()">Step McCabe-Thiele ↗</button><button class="secondary" onclick="resetModule('distil')">Reset inputs</button></div><div id="mc_error" class="error"></div><div id="mc_result" class="result"><div class="result-head"><strong>Distillation column sizing</strong><span>Calculated output</span></div><div id="mc_metrics" class="metrics"></div><div id="mc_plot" class="plot"><img id="mc_img"></div></div></div><div class="helper"><h4>Separation reference</h4><div class="helper-row"><span>Equilibrium</span><b>y = αx / [1+(α−1)x]</b></div><div class="helper-row"><span>Rmin Pinch</span><b>Rmin = (xD-y')/(y'-x')</b></div><div class="helper-row"><span>Reflux</span><b>R = multiplier · Rmin</b></div><div class="helper-row"><span>Output</span><b>Theoretical stages</b></div></div></div></div>

</section><div class="footer">ChemProcess Studio · deterministic process calculations · v2.0</div></main></div>
<script>
const defaults={
    heat:{title:'Heat exchanger rating',sub:'Counter-flow & 1-2 STHE energy balance, LMTD and area.'},
    fluid:{title:'Pipe hydraulics',sub:'Velocity, friction loss, Total Head and pump motor power.'},
    cre:{title:'Reactor sizing & kinetics',sub:'CSTR and PFR volume comparison and residence times.'},
    distil:{title:'Binary distillation',sub:'Theoretical equilibrium stages by McCabe-Thiele.'}
};
function switchTab(name){
    document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab===name));
    document.querySelectorAll('.module').forEach(m=>m.classList.toggle('active',m.id==='module-'+name));
    document.getElementById('workspace-title').textContent=defaults[name].title;
    document.getElementById('workspace-sub').textContent=defaults[name].sub;
}
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>switchTab(b.dataset.tab)));
function updateHotPreset(){const v=document.getElementById('hx_fluid_hot').value,x=document.getElementById('hx_cph');if(v==='custom'){x.readOnly=false;x.focus()}else{x.readOnly=true;x.value=v}}
function updateUPreset(){const v=document.getElementById('hx_service').value,x=document.getElementById('hx_u');if(v==='custom'){x.readOnly=false;x.focus()}else{x.readOnly=true;x.value=v}}
function showError(id,msg){const e=document.getElementById(id+'_error');e.textContent=msg;e.classList.toggle('visible',!!msg)}
function metric(label,value){return `<div class="metric"><span>${label}</span><b>${value}</b></div>`}
async function post(url,payload){const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});return await r.json()}

async function calculateHeat(){
    showError('hx','');
    try{
        const d=await post('/api/heat',{
            hx_type:hx_type.value, m_h:+hx_mh.value, cp_h:+hx_cph.value,
            th_in:+hx_thin.value, th_out:+hx_thout.value, m_c:+hx_mc.value,
            cp_c:4.18, tc_in:+hx_tcin.value, u:+hx_u.value
        });
        if(d.error){showError('hx',d.error);return;}
        hx_metrics.innerHTML=metric('Heat duty',d.q.toFixed(2)+' kW')+
                             metric('Cold outlet',d.tc_out.toFixed(2)+' °C')+
                             metric('Ft factor',d.ft.toFixed(3))+
                             metric('Effective ΔT',d.dt_eff.toFixed(2)+' °C')+
                             metric('LMTD',d.lmtd.toFixed(2)+' °C')+
                             metric('Required area',d.area.toFixed(2)+' m²');
        hx_result.classList.add('visible');
        hx_img.src='data:image/png;base64,'+d.plot;
        hx_plot.classList.add('visible');
    }catch(e){showError('hx','Unable to reach the calculation engine.');}
}

async function calculateFluid(){
    showError('fl','');
    try{
        const d=await post('/api/fluid',{
            d:+fl_d.value, l:+fl_l.value, q_m3h:+fl_q.value,
            rho:+fl_rho.value, mu:+fl_mu.value, eps_mm:+fl_roughness.value,
            dz:+fl_dz.value, kminor:+fl_kminor.value, eta:+fl_eta.value
        });
        if(d.error){showError('fl',d.error);return;}
        fl_metrics.innerHTML=metric('Mean velocity',d.v_avg.toFixed(3)+' m/s')+
                             metric('Reynolds / regime',d.re.toFixed(0)+' · '+d.regime)+
                             metric('Pressure drop',d.dp_kpa.toFixed(2)+' kPa')+
                             metric('Total Head (TDH)',d.tdh.toFixed(2)+' m')+
                             metric('Hydraulic power',d.p_hyd_kw.toFixed(2)+' kW')+
                             metric('Brake power',d.p_brake_kw.toFixed(2)+' kW ('+d.p_brake_hp.toFixed(2)+' HP)');
        fl_result.classList.add('visible');
        fl_img.src='data:image/png;base64,'+d.plot;
        fl_plot.classList.add('visible');
    }catch(e){showError('fl','Unable to reach the calculation engine.');}
}

async function calculateCRE(){
    showError('cre','');
    try{
        const d=await post('/api/cre',{
            order:+cre_order.value, v0:+cre_v0.value,
            ca0:+cre_ca0.value, k:+cre_k.value, xa:+cre_xa.value
        });
        if(d.error){showError('cre',d.error);return;}
        cre_metrics.innerHTML=metric('Target conversion',(d.xa*100).toFixed(1)+' %')+
                              metric('Residual Ca',d.ca_final.toFixed(3)+' mol/L')+
                              metric('CSTR volume',d.cstr_m3.toFixed(2)+' m³ ('+d.tau_cstr.toFixed(1)+' s)')+
                              metric('PFR volume',d.pfr_m3.toFixed(2)+' m³ ('+d.tau_pfr.toFixed(1)+' s)')+
                              metric('Volume ratio (CSTR/PFR)',d.ratio.toFixed(2)+'x');
        cre_result.classList.add('visible');
        cre_img.src='data:image/png;base64,'+d.plot;
        cre_plot.classList.add('visible');
    }catch(e){showError('cre','Unable to reach the calculation engine.');}
}

async function calculateDistil(){
    showError('mc','');
    try{
        const d=await post('/api/distil',{
            zf:+mc_zf.value, xd:+mc_xd.value, xb:+mc_xb.value,
            alpha:+mc_alpha.value, q:+mc_q.value, rmult:+mc_rmult.value
        });
        if(d.error){showError('mc',d.error);return;}
        mc_metrics.innerHTML=metric('Theoretical stages',d.stages+' Trays')+
                             metric('Optimal feed stage','Tray '+d.feed_stage)+
                             metric('Minimum reflux (Rmin)',d.rmin.toFixed(3))+
                             metric('Operating reflux (R)',d.r.toFixed(3))+
                             metric('Distillate ratio (D/F)',(d.d_f*100).toFixed(1)+' %')+
                             metric('Bottoms ratio (B/F)',(d.b_f*100).toFixed(1)+' %');
        mc_result.classList.add('visible');
        mc_img.src='data:image/png;base64,'+d.plot;
        mc_plot.classList.add('visible');
    }catch(e){showError('mc','Unable to reach the calculation engine.');}
}

function resetModule(name){
    const m=document.getElementById('module-'+name);
    m.querySelectorAll('input').forEach(i=>i.value=i.defaultValue);
    m.querySelectorAll('select').forEach(s=>s.selectedIndex=0);
    m.querySelectorAll('.result,.plot,.error').forEach(e=>e.classList.remove('visible'));
    if(name==='heat'){updateHotPreset();updateUPreset();}
}
</script>
</body></html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# 1. HEAT EXCHANGER (COUNTER-FLOW & 1-2 STHE WITH FT CORRECTION)
@app.route('/api/heat', methods=['POST'])
def api_heat():
    d = request.json
    hx_type = d.get('hx_type', 'counter')
    m_h, cp_h = d['m_h'], d['cp_h']
    th_in, th_out = d['th_in'], d['th_out']
    m_c, cp_c = d['m_c'], d['cp_c']
    tc_in = d['tc_in']
    u = d['u']

    q = m_h * cp_h * (th_in - th_out)
    if q <= 0:
        return jsonify({'error': 'Hot fluid outlet must be colder than inlet.'})

    tc_out = tc_in + (q / (m_c * cp_c))
    dt1 = th_in - tc_out
    dt2 = th_out - tc_in

    if dt1 <= 0 or dt2 <= 0:
        return jsonify({'error': f'Thermodynamic crossover: cold fluid exits at {tc_out:.1f}°C, exceeding the hot-stream limit.'})

    lmtd = dt1 if abs(dt1 - dt2) < 1e-5 else (dt1 - dt2) / math.log(dt1 / dt2)

    ft = 1.0
    if hx_type == '1-2':
        R = (th_in - th_out) / (tc_out - tc_in)
        P = (tc_out - tc_in) / (th_in - tc_in)
        if P >= 1.0 or (R * P) >= 1.0:
            return jsonify({'error': 'Selected temperatures exceed 1-2 STHE limits (P >= 1). Choose Counter-Flow.'})
        denom_term = math.sqrt(R**2 + 1)
        term_num = denom_term * math.log((1 - P) / (1 - P * R))
        val = (2 - P * (R + 1 - denom_term)) / (2 - P * (R + 1 + denom_term))
        if val <= 0:
            return jsonify({'error': 'Temperature cross too steep for 1 shell pass (Ft undefined). Use Counter-Flow.'})
        term_den = (R - 1) * math.log(val) if abs(R - 1) > 1e-4 else 2 * P * denom_term / (2 - P)
        ft = term_num / term_den
        if ft < 0.75:
            return jsonify({'error': f'Calculated Ft = {ft:.2f} (< 0.75). Inefficient design: requires 2 or more shell passes.'})

    dt_eff = ft * lmtd
    area = (q * 1000.0) / (u * dt_eff)

    fig, ax = plt.subplots(figsize=(6, 3.4), facecolor='#122238')
    ax.set_facecolor('#091321')
    ax.plot([0, 1], [th_in, th_out], color='#ff7d75', linewidth=2.2, label=f'Hot fluid ({th_in}°C → {th_out}°C)')
    ax.plot([0, 1], [tc_out, tc_in], color='#6ba8ff', linewidth=2.2, label=f'Cold water ({tc_out:.1f}°C ← {tc_in}°C)')
    ax.set_title(f'Axial temperature gradients ({hx_type.upper()}, Ft={ft:.3f})', color='#f5f7fb', fontsize=11)
    ax.set_xlabel('Normalized exchanger path', color='#8d9aaf', fontsize=10)
    ax.set_ylabel('Temperature (°C)', color='#8d9aaf', fontsize=10)
    ax.tick_params(colors='#8d9aaf')
    ax.grid(True, linestyle='--', alpha=0.2, color='#8d9aaf')
    ax.legend(facecolor='#122238', edgecolor='#20324a', labelcolor='#f5f7fb', fontsize=9)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), dpi=120)
    plt.close(fig)
    buf.seek(0)

    return jsonify({
        'q': q, 'tc_out': tc_out, 'dt1': dt1, 'dt2': dt2,
        'lmtd': lmtd, 'ft': ft, 'dt_eff': dt_eff, 'area': area,
        'plot': base64.b64encode(buf.getvalue()).decode()
    })

# 2. FLUID MECHANICS & PUMP SIZING
@app.route('/api/fluid', methods=['POST'])
def api_fluid():
    d = request.json
    dia, length = d['d'], d['l']
    q_m3h = d['q_m3h']
    rho, mu = d['rho'], d['mu']
    eps = d['eps_mm'] / 1000.0
    dz = d.get('dz', 0.0)
    kminor = d.get('kminor', 0.0)
    eta = max(d.get('eta', 0.70), 0.01)

    area_pipe = math.pi * dia**2 / 4.0
    q_m3s = q_m3h / 3600.0
    v_avg = q_m3s / area_pipe
    re = rho * v_avg * dia / mu

    if re < 2100:
        regime = 'Laminar'
        f = 64.0 / re
    elif re < 4000:
        regime = 'Transitional'
        f = 0.032
    else:
        regime = 'Turbulent'
        f = 0.25 / (math.log10(eps / (3.7 * dia) + 5.74 / (re**0.9))**2)

    dp_friction = f * (length / dia) * (rho * v_avg**2 / 2.0)
    dp_minor = kminor * (rho * v_avg**2 / 2.0)
    dp_total_pa = dp_friction + dp_minor
    dp_kpa = dp_total_pa / 1000.0

    hf_m = dp_total_pa / (rho * 9.81)
    tdh = dz + hf_m

    p_hyd_kw = (rho * 9.81 * q_m3s * tdh) / 1000.0
    p_brake_kw = p_hyd_kw / eta
    p_brake_hp = p_brake_kw * 1.34102

    radius_max = dia / 2.0
    r = np.linspace(-radius_max, radius_max, 120)
    if re < 2100:
        u = 2 * v_avg * (1 - (r / radius_max)**2)
    else:
        u = 1.22 * v_avg * (1 - np.abs(r) / radius_max)**(1 / 7.0)

    fig, ax = plt.subplots(figsize=(6, 3.4), facecolor='#122238')
    ax.set_facecolor('#091321')
    ax.plot(u, r * 1000, color='#54e0c1', linewidth=2.2)
    ax.axhline(0, color='#334a64', linestyle=':', alpha=0.6)
    ax.set_title(f'Radial velocity profile ({regime}, Re={re:.0f})', color='#f5f7fb', fontsize=11)
    ax.set_xlabel('Local velocity u(r) [m/s]', color='#8d9aaf', fontsize=10)
    ax.set_ylabel('Radial distance [mm]', color='#8d9aaf', fontsize=10)
    ax.tick_params(colors='#8d9aaf')
    ax.grid(True, linestyle='--', alpha=0.2, color='#8d9aaf')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), dpi=120)
    plt.close(fig)
    buf.seek(0)

    return jsonify({
        'v_avg': v_avg, 're': re, 'regime': regime, 'f': f,
        'dp_kpa': dp_kpa, 'tdh': tdh, 'p_hyd_kw': p_hyd_kw,
        'p_brake_kw': p_brake_kw, 'p_brake_hp': p_brake_hp,
        'plot': base64.b64encode(buf.getvalue()).decode()
    })

# 3. CONTINUOUS REACTOR ENGINEERING (CSTR VS PFR)
@app.route('/api/cre', methods=['POST'])
def api_cre():
    d = request.json
    order = int(d['order'])
    v0_m3h = d.get('v0', 5.0)
    ca0, k, xa = d['ca0'], d['k'], d['xa']

    if xa >= 1.0 or xa <= 0:
        return jsonify({'error': 'Target conversion X_A must be between 0 and 0.99.'})

    v0_m3s = v0_m3h / 3600.0
    ca_final = ca0 * (1.0 - xa)

    if order == 0:
        tau_pfr = (ca0 * xa) / k
        tau_cstr = (ca0 * xa) / k
    elif order == 1:
        tau_pfr = -math.log(1.0 - xa) / k
        tau_cstr = xa / (k * (1.0 - xa))
    elif order == 2:
        tau_pfr = xa / (k * ca0 * (1.0 - xa))
        tau_cstr = xa / (k * ca0 * (1.0 - xa)**2)
    else:
        return jsonify({'error': 'Unsupported reaction order.'})

    pfr_m3 = v0_m3s * tau_pfr
    cstr_m3 = v0_m3s * tau_cstr
    ratio = (cstr_m3 / pfr_m3) if pfr_m3 > 0 else 1.0

    t_span = max(tau_pfr * 1.35, 1.0)
    t = np.linspace(0, t_span, 200)
    if order == 0:
        ca_curve = np.maximum(0, ca0 - k * t)
    elif order == 1:
        ca_curve = ca0 * np.exp(-k * t)
    else:
        ca_curve = ca0 / (1 + k * ca0 * t)

    fig, ax = plt.subplots(figsize=(6, 3.4), facecolor='#122238')
    ax.set_facecolor('#091321')
    ax.plot(t, ca_curve, color='#54e0c1', linewidth=2.2, label=f'Order {order} decay')
    ax.scatter([tau_pfr], [ca_final], color='#ff7d75', s=50, zorder=5, label=f'PFR Target Xₐ={xa*100:.0f}%')
    ax.axvline(tau_pfr, color='#ff7d75', linestyle='--', alpha=0.4)
    ax.axhline(ca_final, color='#ff7d75', linestyle='--', alpha=0.4)
    ax.set_title(f'Kinetics (CSTR={cstr_m3:.2f}m³, PFR={pfr_m3:.2f}m³)', color='#f5f7fb', fontsize=11)
    ax.set_xlabel('PFR Residence time τ (s)', color='#8d9aaf', fontsize=10)
    ax.set_ylabel('Reactant conc. C_A (mol/L)', color='#8d9aaf', fontsize=10)
    ax.tick_params(colors='#8d9aaf')
    ax.grid(True, linestyle='--', alpha=0.2, color='#8d9aaf')
    ax.legend(facecolor='#122238', edgecolor='#20324a', labelcolor='#f5f7fb', fontsize=8.5)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), dpi=120)
    plt.close(fig)
    buf.seek(0)

    return jsonify({
        'xa': xa, 'ca_final': ca_final, 'order': order,
        'tau_pfr': tau_pfr, 'tau_cstr': tau_cstr,
        'pfr_m3': pfr_m3, 'cstr_m3': cstr_m3, 'ratio': ratio,
        'plot': base64.b64encode(buf.getvalue()).decode()
    })

# 4. MCCABE-THIELE DISTILLATION SOLVER & STEPPING
@app.route('/api/distil', methods=['POST'])
def api_distil():
    d = request.json
    zf, xd, xb = d['zf'], d['xd'], d['xb']
    alpha, q, rmult = d['alpha'], d['q'], d['rmult']

    if not (0 < xb < zf < xd < 1) or alpha <= 1.0 or rmult <= 1.0:
        return jsonify({'error': 'Ensure 0 < xB < zF < xD < 1, alpha > 1.0, and reflux multiplier > 1.0.'})

    def y_eq(x):
        return (alpha * x) / (1.0 + (alpha - 1.0) * x)

    def x_eq(y):
        return y / (alpha - (alpha - 1.0) * y)

    d_f = (zf - xb) / (xd - xb)
    b_f = 1.0 - d_f

    # q-line intersection with equilibrium curve
    if abs(q - 1.0) < 1e-4:
        xi = zf
        yi = y_eq(xi)
    elif abs(q) < 1e-4:
        yi = zf
        xi = x_eq(yi)
    else:
        A_q = (q / (q - 1.0)) * (alpha - 1.0)
        B_q = (q / (q - 1.0)) - (zf / (q - 1.0)) * (alpha - 1.0) - alpha
        C_q = - zf / (q - 1.0)
        disc = max(0, B_q**2 - 4 * A_q * C_q)
        xi = (-B_q - math.sqrt(disc)) / (2 * A_q)
        yi = y_eq(xi)

    slope_min = (xd - yi) / (xd - xi)
    if slope_min >= 1.0 or slope_min <= 0:
        return jsonify({'error': 'Infeasible separation pinch point. Check q and volatility values.'})

    rmin = slope_min / (1.0 - slope_min)
    r = rmin * rmult

    rol_m = r / (r + 1.0)
    rol_c = xd / (r + 1.0)

    if abs(q - 1.0) < 1e-4:
        x_cross = zf
        y_cross = rol_m * x_cross + rol_c
    else:
        x_cross = (rol_c + zf / (q - 1.0)) / ((q / (q - 1.0)) - rol_m)
        y_cross = rol_m * x_cross + rol_c

    sol_m = (y_cross - xb) / (x_cross - xb)
    sol_c = xb - sol_m * xb

    stages = 0
    feed_stage = 1
    curr_x = xd
    curr_y = xd
    x_steps = [curr_x]
    y_steps = [curr_y]

    while curr_x > xb and stages < 60:
        stages += 1
        curr_x = x_eq(curr_y)
        x_steps.extend([curr_x, curr_x])
        if curr_x > x_cross:
            curr_y = rol_m * curr_x + rol_c
            feed_stage = stages + 1
        else:
            curr_y = sol_m * curr_x + sol_c
        y_steps.extend([y_steps[-1], curr_y])

    xx = np.linspace(0, 1, 150)
    fig, ax = plt.subplots(figsize=(6, 4.4), facecolor='#122238')
    ax.set_facecolor('#091321')
    ax.plot(xx, xx, color='#445773', linestyle=':', label='y = x')
    ax.plot(xx, y_eq(xx), color='#d99a2b', linewidth=2.2, label='VLE curve')
    ax.plot([x_cross, xd], [y_cross, xd], color='#ff7d75', linewidth=1.8, label=f'ROL (R={r:.2f})')
    ax.plot([xb, x_cross], [xb, y_cross], color='#54e0c1', linewidth=1.8, label='SOL (Stripping)')
    ax.plot([zf, x_cross], [zf, y_cross], color='#6ba8ff', linestyle='--', label=f'q-line (q={q:.1f})')
    ax.plot(x_steps, y_steps, color='#f2f2f0', linewidth=1.3, label=f'Trays ({stages})')

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_title(f'McCabe-Thiele ({stages} Stages, Feed @ Stage {feed_stage})', color='#f5f7fb', fontsize=11)
    ax.set_xlabel('Liquid mole fraction x', color='#8d9aaf', fontsize=10)
    ax.set_ylabel('Vapor mole fraction y', color='#8d9aaf', fontsize=10)
    ax.tick_params(colors='#8d9aaf')
    ax.grid(True, linestyle='--', alpha=0.18, color='#8d9aaf')
    ax.legend(facecolor='#122238', edgecolor='#20324a', labelcolor='#f5f7fb', fontsize=8, loc='lower right')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=fig.get_facecolor(), dpi=120)
    plt.close(fig)
    buf.seek(0)

    return jsonify({
        'rmin': rmin, 'r': r, 'stages': stages,
        'feed_stage': feed_stage, 'd_f': d_f, 'b_f': b_f,
        'plot': base64.b64encode(buf.getvalue()).decode()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8501)), debug=False)
