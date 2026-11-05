layout(location=0) in vec3 vertexPosition;
in vec2 vertexUV;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
out vec2 UV;
void main(){UV=vertexUV;gl_Position=projectionMatrix*viewMatrix*modelMatrix*vec4(vertexPosition,1);}
