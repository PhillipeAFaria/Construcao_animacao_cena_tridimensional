// Prepara posições em recorte e em mundo, normais, cor, UV e posição relativa à luz.

            // M transforma para mundo, V para vista e P para o espaço de recorte.
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            // A posição usa o índice zero também no shader de profundidade.
            layout(location=0) in vec3 vertexPosition;
            in vec2 vertexUV;
            in vec3 vertexNormal;
            in vec3 vertexColor;
            out vec3 interpolatedColor;
            uniform vec2 repeatUV;
            uniform vec2 offsetUV;
            out vec3 position;
            out vec2 UV;
            out vec3 normal;
            
            struct Shadow
            {
                // direction of light that casts shadow
                vec3 lightDirection;
                // data from camera that produces depth texture
                mat4 projectionMatrix;
                mat4 viewMatrix;
                // texture that stores depth values from shadow camera
                sampler2D depthTextureSampler;
                // regions in shadow multiplied by (1-strength)
                float strength;
                // reduces unwanted visual artifacts
                float bias;
            };
            
            uniform bool useShadow;
            uniform Shadow shadow0;
            out vec3 shadowPosition0;

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
                position = vec3(modelMatrix * vec4(vertexPosition, 1));
                UV = vertexUV * repeatUV + offsetUV;
                interpolatedColor = vertexColor;
                // A inversa transposta corrige a normal quando a escala muda por eixo.
                normal = normalize(transpose(inverse(mat3(modelMatrix))) * vertexNormal);
                
                // A segunda transformação projeta o mesmo vértice do ponto de vista da luz.
                if (useShadow)
                {
                    vec4 temp0 = shadow0.projectionMatrix * shadow0.viewMatrix * modelMatrix * vec4(vertexPosition, 1);
                    shadowPosition0 = vec3(temp0);
                } 
            }
        
