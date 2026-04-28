// 着色郡 · GLSL fragment shader（象征性）
//
// 角色：specialist · specialty=celestial-omen
// 真实渲染由 run.py 用 Python 模拟（生成 SVG artifact）；
// 此文件保留 GLSL 原文，作为天象之礼器。

#version 330 core

uniform float u_time;
uniform vec2  u_resolution;
uniform float u_seed;

out vec4 frag_color;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution;
    float r = length(uv - 0.5);
    float omen = smoothstep(0.45, 0.5, r) * (0.6 + 0.4 * hash(uv * u_seed));
    vec3 col = mix(vec3(0.05, 0.0, 0.1), vec3(1.0, 0.85, 0.4), omen);
    col += 0.08 * sin(u_time + r * 30.0);
    frag_color = vec4(col, 1.0);
}
