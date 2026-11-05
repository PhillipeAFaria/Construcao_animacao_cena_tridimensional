in vec2 UV;
out vec4 fragColor;
float cloud(vec2 center,vec2 size){return 1.0-smoothstep(0.55,1.0,length((UV-center)/size));}
void main(){
    vec3 color=mix(vec3(.58,.70,.68),vec3(.14,.30,.38),smoothstep(0.0,1.0,UV.y));
    float haze=cloud(vec2(.14,.78),vec2(.17,.032))+cloud(vec2(.22,.79),vec2(.13,.04))
              +cloud(vec2(.73,.69),vec2(.20,.025));
    color=mix(color,vec3(.77,.82,.75),clamp(haze*.24,0,0.3));
    fragColor=vec4(color,1);
}
