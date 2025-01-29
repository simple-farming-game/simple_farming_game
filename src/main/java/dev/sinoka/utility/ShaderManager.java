package dev.sinoka.utility;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.HashMap;
import java.util.Map;
import static org.lwjgl.opengl.GL20.*;

public class ShaderManager {
    private static ShaderManager instance;
    private Shader defaultShader;
    private final Map<String, Shader> shaderMap = new HashMap<>();
    private static final Logger logger = LogManager.getLogger(ShaderManager.class);

    private ShaderManager() {
        // 생성자에서 `loadDefaultShader()` 호출 제거 → 명시적으로 호출 필요
    }

    public static ShaderManager getInstance() {
        if (instance == null) {
            instance = new ShaderManager();
        }
        return instance;
    }

    public void loadDefaultShader() {
        if (defaultShader == null) {
            logger.debug("🚀 Loading Default Shader...");
            defaultShader = new Shader(
                    ResourceUtil.getAbsolutePath("shader/vertex.glsl"),
                    ResourceUtil.getAbsolutePath("shader/fragment.glsl")
            );
            shaderMap.put("default", defaultShader);
            logger.debug("✅ Default Shader Loaded Successfully!");
        }
    }

    public Shader getDefaultShader() {
        if (defaultShader == null) {
            loadDefaultShader(); // 🚀 기본 쉐이더가 없으면 자동 로드
        }
        return defaultShader;
    }

    public void useDefaultShader() {
        useShader("default");
    }

    public void loadShader(String name, String vertexPath, String fragmentPath) {
        if (!shaderMap.containsKey(name)) {
            Shader shader = new Shader(ResourceUtil.getAbsolutePath(vertexPath), ResourceUtil.getAbsolutePath(fragmentPath));
            shaderMap.put(name, shader);
            logger.debug("✅ Loaded Shader: " + name);
        } else {
            System.err.println("⚠️ Shader '" + name + "' is already loaded!");
        }
    }

    public Shader getShader(String name) {
        if (shaderMap.containsKey(name)) {
            return shaderMap.get(name);
        } else {
            System.err.println("❌ Shader '" + name + "' not found! Using default shader.");
            return getDefaultShader();
        }
    }

    public void useShader(String name) {
        Shader shader = getShader(name);
        if (shader != null) {
            shader.use();
        }
    }

    public void printLoadedShaders() {
        if (shaderMap.isEmpty()) {
            System.out.println("No shaders loaded.");
        } else {
            System.out.println("Loaded Shaders:");
            for (String shaderName : shaderMap.keySet()) {
                System.out.println("- " + shaderName);
            }
        }
    }

    public void cleanup() {
        for (Shader shader : shaderMap.values()) {
            shader.delete();
        }
        shaderMap.clear();
        logger.debug("✅ All shaders deleted.");
    }
}
