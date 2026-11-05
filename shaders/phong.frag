        
            struct Light
            {
                int lightType;  // 1 = AMBIENT, 2 = DIRECTIONAL, 3 = POINT
                vec3 color;  // used by all lights
                vec3 direction;  // used by point lights
                vec3 position;  // used by point lights
                vec3 attenuation;  // used by point lights
            };


			uniform Light light0;
			uniform Light light1;

            uniform vec3 viewPosition;
            uniform float specularStrength;
            uniform float shininess;

            vec3 calculateLight(Light light, vec3 pointPosition, vec3 pointNormal)
            {
                float ambient = 0;
                float diffuse = 0;
                float specular = 0;
                float attenuation = 1;
                vec3 lightDirection = vec3(0, 0, 0);
                
                if (light.lightType == 1)  // ambient light
                {
                    ambient = 1;
                }
                else if (light.lightType == 2)  // directional light
                {
                    lightDirection = normalize(light.direction);
                }
                else if (light.lightType == 3)  // point light
                {
                    lightDirection = normalize(pointPosition - light.position);
                    float distance = length(light.position - pointPosition);
                    attenuation = 1.0 / (light.attenuation[0] 
                                       + light.attenuation[1] * distance 
                                       + light.attenuation[2] * distance * distance);
                }
                
                if (light.lightType > 1)  // directional or point light
                {
                    pointNormal = normalize(pointNormal);
                    diffuse = max(dot(pointNormal, -lightDirection), 0.0);
                    diffuse *= attenuation;
                    if (diffuse > 0)
                    {
                        vec3 viewDirection = normalize(viewPosition - pointPosition);
                        vec3 reflectDirection = reflect(lightDirection, pointNormal);
                        specular = max(dot(viewDirection, reflectDirection), 0.0);
                        specular = specularStrength * pow(specular, shininess);
                    }
                }
                return light.color * (ambient + diffuse + specular);
            }

            uniform vec3 baseColor;
            uniform bool useVertexColors;
            uniform float focusFactor;
            uniform bool grayScale;
            uniform float scannerActive;
            uniform vec3 scannerPosition;
            uniform vec3 scannerDirection;
            uniform vec3 scannerColor;
            in vec3 interpolatedColor;
            uniform bool useTexture;
            uniform sampler2D textureSampler;
            uniform bool useBumpTexture;
            uniform sampler2D bumpTextureSampler;
            uniform float bumpStrength;
            in vec3 position;
            in vec2 UV;
            in vec3 normal;
            out vec4 fragColor;
            
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
            in vec3 shadowPosition0;

            void main()
            {
                vec4 color = vec4(baseColor, 1.0);
                if (useVertexColors)
                    color.rgb *= interpolatedColor;
                if (useTexture) 
                {
                    color *= texture(textureSampler, UV );
                }
                vec3 calcNormal = normal;
                vec3 surfaceColor=color.rgb;
                if (useBumpTexture) 
                {
                    calcNormal += bumpStrength * vec3(texture(bumpTextureSampler, UV));
                }
                // Calculate total effect of lights on color
                vec3 light = vec3(0, 0, 0);
				light += calculateLight(light0, position, calcNormal);
				light += calculateLight(light1, position, calcNormal);
                color *= vec4(light, 1);
                
                if (useShadow)
                {
                    // determine if surface is facing towards light direction
                    float cosAngle = dot(normalize(normal), -normalize(shadow0.lightDirection));
                    bool facingLight = (cosAngle > 0.01);
                    // convert range [-1, 1] to range [0, 1]
                    // for UV coordinate and depth information
                    vec3 shadowCoord = (shadowPosition0.xyz + 1.0) / 2.0;
                    bool insideMap = all(greaterThanEqual(shadowCoord, vec3(0))) && all(lessThanEqual(shadowCoord, vec3(1)));
                    if (insideMap && facingLight)
                    {
                        vec2 texel = 1.0 / vec2(textureSize(shadow0.depthTextureSampler, 0));
                        // Slope-aware tolerance reduces acne at grazing angles.
                        float bias = max(shadow0.bias * (1.0 - cosAngle), shadow0.bias * 0.35);
                        float coverage = 0.0;
                        for (int x = -1; x <= 1; x++)
                            for (int y = -1; y <= 1; y++)
                            {
                                float closest = texture(shadow0.depthTextureSampler, shadowCoord.xy + vec2(x,y)*texel).r;
                                coverage += (shadowCoord.z > closest + bias) ? 1.0 : 0.0;
                            }
                        color.rgb *= 1.0 - shadow0.strength * coverage / 9.0;
                    }
                }  
                
                // Recognition light: smooth spotlight from the rover sensor.
                if (scannerActive>0.0) {
                    vec3 ray=position-scannerPosition;
                    float distanceToSensor=length(ray);
                    float angle=dot(normalize(ray),normalize(scannerDirection));
                    float cone=smoothstep(cos(0.20),cos(0.11),angle);
                    float falloff=max(0.0,1.0-distanceToSensor/6.0);
                    float diffuse=max(dot(normalize(calcNormal),-normalize(ray)),0.0);
                    color.rgb+=surfaceColor*scannerColor*scannerActive*cone*falloff*(0.3+1.8*diffuse);
                }
                // Perceptual comparison, not a clinical model of human vision.
                float luminance = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
                color.rgb = mix(vec3(luminance), color.rgb, focusFactor);
                color.rgb *= mix(0.60, 1.0, focusFactor);
                if (grayScale)
                    color.rgb = vec3(dot(color.rgb, vec3(0.2126, 0.7152, 0.0722)));
                fragColor = color;
            }
        
