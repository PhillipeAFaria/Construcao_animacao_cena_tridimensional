// Calcula a transparência do cone, do núcleo e do halo antes da mistura aditiva.
in vec2 UV;
uniform vec3 glowColor;
uniform float intensity;
uniform float effectTime;
uniform int beamMode;
out vec4 fragColor;
void main() {
    float alpha;
    // O halo perde intensidade do centro para a borda. Os outros modos usam o eixo do feixe.
    if (beamMode==2) {
        float radius=length(UV*2.0-1.0);
        alpha=pow(max(0.0,1.0-radius),2.0)*0.85;
    } else {
        float fade=1.0-smoothstep(0.72,1.0,UV.y);
        // O tempo da simulação desloca o padrão luminoso, inclusive com pausa.
        float scan=0.8+0.2*sin(UV.y*36.0-effectTime*4.0);
        alpha=fade*scan*(beamMode==0 ? 0.13 : 0.72);
    }
    fragColor=vec4(glowColor,alpha*intensity);
}
