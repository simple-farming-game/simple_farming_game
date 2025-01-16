#version 330 core

layout (location = 0) in vec2 aPos;

uniform mat4 model;
uniform vec2 uTexRegion;
uniform vec2 uTexSize;
uniform mat4 projection;
uniform mat4 view;

out vec2 TexCoord;

void main() {
    // 월드 좌표로 변환
    gl_Position = projection * view * model * vec4(aPos, 0, 1.0);

    // 텍스처 좌표 계산 (경계 보정)
    vec2 baseTexCoord = vec2(clamp((aPos.x + 1.0) / 2.0, 0.0, 1.0),
    clamp((aPos.y + 1.0) / 2.0, 0.0, 1.0));
    TexCoord = uTexRegion + baseTexCoord * uTexSize;
}
