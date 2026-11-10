// Usa o mesmo atributo de posição das malhas Phong. A vista e a projeção vêm da câmera da luz.

        layout(location=0) in vec3 vertexPosition;
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        