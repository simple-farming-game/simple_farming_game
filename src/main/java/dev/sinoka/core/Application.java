package dev.sinoka.core;

import dev.sinoka.block.Block;
import dev.sinoka.block.BlockBuilder;
import dev.sinoka.entity.Player;
import dev.sinoka.utility.Camera;
import dev.sinoka.utility.ResourceUtil;
import dev.sinoka.utility.ShaderManager;
import dev.sinoka.utility.Texture;
import dev.sinoka.world.MapData;
import dev.sinoka.world.World;
import org.joml.Vector3f;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.lwjgl.opengl.GL;

public class Application {
    private WindowManager windowManager;
    private GameLoop gameLoop;
    private Camera camera;
    private Player player;
    private ShaderManager shaderManager;
    private World world;
    private static final Logger logger = LogManager.getLogger(Application.class);

    public Application() {
        logger.debug("🚀 Initializing Application...");

        // 🚀 1️⃣ 초기화 순서 변경: OpenGL 컨텍스트가 생성되기 전에는 리소스 로딩 금지
        this.player = new Player(new Vector3f(0, 5.0f, 0));
        this.camera = new Camera(new Vector3f(player.getPos().x, player.getPos().y + 1f, player.getPos().z));
        this.world = new World();
    }

    public void run() {
        logger.debug("🚀 Initializing game resources...");

        // 🚀 2️⃣ OpenGL 컨텍스트 생성 후 리소스 로드
        windowManager = new WindowManager(camera);
        windowManager.init(); // OpenGL 컨텍스트 생성

        logger.debug("✅ OpenGL context initialized!");

        // 🚀 3️⃣ OpenGL 컨텍스트 생성 후 ShaderManager 및 리소스 로드
        this.shaderManager = ShaderManager.getInstance();
        shaderManager.loadDefaultShader(); // ✅ 기본 쉐이더 로드
        shaderManager.loadShader("text", "shader/textVertex.glsl", "shader/textFragment.glsl");

        registerBlocks();
        createTestMap();

        logger.debug("✅ Resource loading complete!");

        // 🚀 4️⃣ 게임 루프 시작
        this.gameLoop = new GameLoop(windowManager, camera, player, world);

        gameLoop.start();
    }

    private void registerBlocks() {
        logger.debug("🔹 Registering blocks...");

        // 🚀 5️⃣ OpenGL 컨텍스트가 생성된 후 텍스처 로드 (필수)
        Texture grassTexture = new Texture(ResourceUtil.getAbsolutePath("image/grass.png"));
        Block grassBlock = new BlockBuilder()
                .setBlockID("grassBlock")
                .setStrength(1)
                .setBreakable(true)
                .setTextureID(grassTexture)
                .build();

        world.getBlockRegister().register(grassBlock);
        logger.debug("✅ Blocks registered.");
    }

    private void createTestMap() {
        logger.debug("🔹 Creating test map...");

        MapData mapData = new MapData("testing");
        int width = 100, height = 1, depth = 100;

        for (int x = 0; x < width; x++) {
            for (int z = 0; z < depth; z++) {
                for (int y = 0; y < height; y++) {
                    mapData.setBlockAt(x, y, z, "grassBlock");
                }
            }
        }

        world.addMap(mapData);
        logger.debug("✅ Test map created.");
    }
}
