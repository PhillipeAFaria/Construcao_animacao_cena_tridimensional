// Grava gl_FragCoord.z como cor para leitura posterior no shader Phong.

        out vec4 fragColor;
        
        void main()
        {
            float z = gl_FragCoord.z;
            fragColor = vec4(z, z, z, 1);
        }
        