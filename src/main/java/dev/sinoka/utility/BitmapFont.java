package dev.sinoka.utility;

import dev.sinoka.renderer.TextureRenderer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.joml.Vector2f;
import org.json.JSONObject;

import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL30.*;

import java.nio.file.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class BitmapFont {
    private static final float[] VERTICES_KO = {
            -235.0f,  235.0f,  // 왼쪽 위 (-470/2, +470/2)
            -235.0f, -235.0f,  // 왼쪽 아래 (-470/2, -470/2)
            235.0f, -235.0f,   // 오른쪽 아래 (+470/2, -470/2)
            235.0f,  235.0f    // 오른쪽 위 (+470/2, +470/2)
    };
    private static final float[] VERTICES_EN = {-50.0f, 50.0f, -50.0f, -50.0f, 50.0f, -50.0f, 50.0f, 50.0f};
    private static final int[] INDICES = {1, 2, 0, 0, 3, 2};

    private final int VAO_EN;
    private final int VBO_EN;
    private final int EBO_EN;
    private final int VBO_KO;
    private final int EBO_KO;
    private final int VAO_KO;
    private Shader shaderProgram;
    private List<String> enText;
    private List<String> koText;

    private int screenWidth;
    private int screenHeight;

    private Map<Character, Glyph> glyphs = new HashMap<>();

    private static final Logger logger = LogManager.getLogger(BitmapFont.class);

    private final int TEXTURE_WIDTH_EN;
    private final int TEXTURE_HEIGHT_EN;

    private final int TEXTURE_WIDTH_KO;
    private final int TEXTURE_HEIGHT_KO;

    private final int GLYPH_SIZE;


    // 글리프 정보 저장
    static class Glyph {
        Texture textSet;
        int width, height;
        float xOffset, yOffset;
        float xAdvance;
        float spacingFactor;

        public Glyph(Texture textTexture, Vector2f glyphSize, float xOffset, float yOffset, float xAdvance, float spacingFactor) {
            this.textSet = textTexture;
            this.width = (int) glyphSize.x;
            this.height = (int) glyphSize.y;
            this.xOffset = xOffset;
            this.yOffset = yOffset;
            this.xAdvance = xAdvance;
            this.spacingFactor = spacingFactor;
        }
    }

    public BitmapFont(Shader shaderProgram, JsonFileReader JFR) {
        this.shaderProgram = shaderProgram;

        // JSON 데이터 읽기
        JSONObject fontData = JFR.readJson();
        JSONObject fontPathEn = fontData.getJSONObject("fontPath");
        JSONObject fontPathKo = fontData.getJSONObject("fontPath");

        // 영어 및 한글 폰트 텍스처 로드
        List<Texture> texturesEn = new ArrayList<>();
        for (Object path : fontPathEn.getJSONArray("en-us").toList()) {
            texturesEn.add(new Texture(ResourceUtil.getAbsolutePath(path.toString())));
        }

        List<Texture> texturesKo = new ArrayList<>();
        for (Object path : fontPathKo.getJSONArray("ko-kr").toList()) {
            texturesKo.add(new Texture(ResourceUtil.getAbsolutePath(path.toString())));
        }

        // 기본 간격 설정 (영어 및 한글 개별 적용)
        float defaultSpacingFactorEn = 6.0f;  // 기본값 (영어)
        float defaultSpacingFactorKo = 10.0f; // 기본값 (한글)

        // 텍스트 파일 경로 읽기 (en-us, ko-kr는 리스트로 처리)
        List<String> enTextFilePaths = new ArrayList<>();
        List<String> koTextFilePaths = new ArrayList<>();

        for (Object path : fontData.getJSONObject("textSetPath").getJSONArray("en-us").toList()) {
            enTextFilePaths.add((String) path);
        }

        for (Object path : fontData.getJSONObject("textSetPath").getJSONArray("ko-kr").toList()) {
            koTextFilePaths.add((String) path);
        }

        // 텍스트 파일 읽기
        try {
            // 영어 텍스트 파일 합치기
            List<String> enTextList = new ArrayList<>();
            for (String enTextFilePath : enTextFilePaths) {
                List<String> enTextOrder = Files.readAllLines(Paths.get(ResourceUtil.getAbsolutePath(enTextFilePath)));
                enTextOrder.stream().filter(line -> !line.isEmpty())
                        .forEach(enTextList::add);  // 각 라인을 리스트에 추가
            }
            enText = enTextList; // 영어 텍스트를 리스트로 저장

            // 한글 텍스트 파일 합치기
            List<String> koTextList = new ArrayList<>();
            for (String koTextFilePath : koTextFilePaths) {
                List<String> koTextOrder = Files.readAllLines(Paths.get(ResourceUtil.getAbsolutePath(koTextFilePath)));
                koTextOrder.stream().filter(line -> !line.isEmpty())
                        .forEach(koTextList::add);  // 각 라인을 리스트에 추가
            }
            koText = koTextList; // 한글 텍스트를 리스트로 저장

        } catch (java.io.IOException e) {
            logger.error(e);
        }


        if (fontData.has("default")) {
            JSONObject defaultSpacingFactorData = fontData.getJSONObject("default");
            defaultSpacingFactorEn = (float) defaultSpacingFactorData.getJSONObject("en-us").getDouble("spacingFactor");
            defaultSpacingFactorKo = (float) defaultSpacingFactorData.getJSONObject("ko-kr").getDouble("spacingFactor");
        }

        // 글리프 데이터 로드
        // 영어 텍스처 크기 동적으로 가져오기
        int imageWidthEn = texturesEn.get(0).getWidth();  // 영어 텍스처 이미지의 가로 크기
        int imageHeightEn = texturesEn.get(0).getHeight(); // 영어 텍스처 이미지의 세로 크기

        // 한글 텍스처 크기 동적으로 가져오기
        int imageWidthKo = texturesKo.get(0).getWidth();  // 한글 텍스처 이미지의 가로 크기
        int imageHeightKo = texturesKo.get(0).getHeight(); // 한글 텍스처 이미지의 세로 크기

        TEXTURE_HEIGHT_EN = imageHeightEn;
        TEXTURE_WIDTH_EN = imageWidthEn;

        TEXTURE_HEIGHT_KO = imageHeightKo;
        TEXTURE_WIDTH_KO = imageWidthKo;

        // 글리프 크기
        GLYPH_SIZE = 10; // 글리프 크기

        // 영어 텍스처에 대한 GLYPH_COLUMNS과 GLYPH_ROWS 계산
        final int GLYPH_COLUMNS_EN = imageHeightEn / GLYPH_SIZE;  // 한 줄에 들어가는 영어 글리프의 개수
        final int GLYPH_ROWS_EN = imageWidthEn / GLYPH_SIZE;    // 총 영어 글리프의 행 수

        // 한글 텍스처에 대한 GLYPH_COLUMNS과 GLYPH_ROWS 계산
        final int GLYPH_COLUMNS_KO = imageHeightKo / GLYPH_SIZE;  // 한 줄에 들어가는 한글 글리프의 개수
        final int GLYPH_ROWS_KO = imageWidthKo / GLYPH_SIZE;    // 총 한글 글리프의 행 수

        if (fontData.has("glyphs")) {
            JSONObject glyphData = fontData.getJSONObject("glyphs");

            // 영어 글리프 처리
            for (int j = 0; j < texturesEn.size(); j++) {
                List<Texture> textures = texturesEn;

                for (int i = 0; i < enText.get(j).length(); i++) {
                    char c = enText.get(j).charAt(i);
                    JSONObject glyphInfo = glyphData.optJSONObject(String.valueOf(c));

                    // 기본 값 적용 (JSON에 없는 문자 처리)
                    float spacingFactor = defaultSpacingFactorEn;
                    Vector2f glyphSize = new Vector2f(GLYPH_SIZE, GLYPH_SIZE);
                    int glyphX = i % GLYPH_COLUMNS_EN;
                    int glyphY = i / GLYPH_ROWS_EN;
                    float xOffset = (1f / GLYPH_COLUMNS_EN) * glyphX;
                    float yOffset = 1f - ((1f / GLYPH_ROWS_EN) * (glyphY + 1));
                    float xAdvance = GLYPH_SIZE; // 글리프의 너비

                    if (glyphInfo != null) {
                        spacingFactor = (float) glyphInfo.getDouble("spacingFactor");
                    }

                    // 텍스처 인덱스를 textures 배열에 맞춰서 사용
                    Texture texture = textures.get(j);

                    // 글리프 생성
                    Glyph glyph = new Glyph(texture, glyphSize, xOffset, yOffset, xAdvance, spacingFactor);
                    glyphs.put(c, glyph);  // 한 개의 glyphs 맵에 저장
                }
            }

            // 두 개의 텍스처 배열을 처리하기 위한 2중 for문
            for (int j = 0; j < texturesKo.size(); j++) {
                List<Texture> textures = texturesKo;

                for (int i = 0; i < koText.get(j).length(); i++) {
                    char c = koText.get(j).charAt(i);
                    JSONObject glyphInfo = glyphData.optJSONObject(String.valueOf(c));

                    // 기본 값 적용 (JSON에 없는 문자 처리)
                    float spacingFactor = defaultSpacingFactorKo;
                    Vector2f glyphSize = new Vector2f(GLYPH_SIZE, GLYPH_SIZE);
                    int glyphX = i % GLYPH_COLUMNS_KO;
                    int glyphY = i / GLYPH_ROWS_KO;
                    float xOffset = ((1f / GLYPH_COLUMNS_KO) * glyphX);
                    float yOffset = 1f - ((1f / GLYPH_ROWS_KO) * (glyphY + 1));
                    float xAdvance = GLYPH_SIZE; // 글리프의 너비

                    if (glyphInfo != null) {
                        spacingFactor = (float) glyphInfo.getDouble("spacingFactor");
                    }

                    // 텍스처 인덱스를 textures 배열에 맞춰서 사용
                    Texture texture = textures.get(j);

                    // 글리프 생성
                    Glyph glyph = new Glyph(texture, glyphSize, xOffset, yOffset, xAdvance, spacingFactor);
                    glyphs.put(c, glyph);  // 한 개의 glyphs 맵에 저장
                }
            }
        }

        int attributeSize = 2;
        int stride = attributeSize * Float.BYTES;

        VAO_EN = glGenVertexArrays();  // Generate VAO_EN
        VBO_EN = glGenBuffers();
        EBO_EN = glGenBuffers();

        glBindVertexArray(VAO_EN);
        glBindBuffer(GL_ARRAY_BUFFER, VBO_EN);
        glBufferData(GL_ARRAY_BUFFER, VERTICES_EN, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_EN);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, INDICES, GL_STATIC_DRAW);

        glVertexAttribPointer(0, attributeSize, GL_FLOAT, false, stride, 0);
        glEnableVertexAttribArray(0);
        glBindVertexArray(0); // Unbind VAO_EN

        VAO_KO = glGenVertexArrays();  // Generate VAO_EN
        VBO_KO = glGenBuffers();
        EBO_KO = glGenBuffers();

        glBindVertexArray(VAO_KO);
        glBindBuffer(GL_ARRAY_BUFFER, VBO_KO);
        glBufferData(GL_ARRAY_BUFFER, VERTICES_KO, GL_STATIC_DRAW);

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO_KO);
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, INDICES, GL_STATIC_DRAW);

        glVertexAttribPointer(0, attributeSize, GL_FLOAT, false, stride, 0);
        glEnableVertexAttribArray(0);
        glBindVertexArray(0); // Unbind VAO_EN
    }

    private static boolean isKorean(char c) {
        Character.UnicodeBlock block = Character.UnicodeBlock.of(c);
        return block == Character.UnicodeBlock.HANGUL_COMPATIBILITY_JAMO ||
                block == Character.UnicodeBlock.HANGUL_SYLLABLES ||
                block == Character.UnicodeBlock.HANGUL_JAMO;
    }

    public void renderString(String text, Vector2f position, float scale) {
        float cursorX = position.x;
        float cursorY = position.y;

        for (char c : text.toCharArray()) {
            Glyph glyph = getGlyphForCharacter(c);  // 각 문자의 언어에 맞는 글리프를 가져옵니다.

            if (glyph == null) {
                continue;
            };  // 해당 문자가 글리프에 없다면 무시

            boolean isKo = isKorean(c);

            // 언어에 맞는 텍스처 및 글리프 적용
            renderGlyph(glyph, new Vector2f(cursorX, cursorY), scale, glyph.textSet, isKo ? VAO_KO : VAO_EN, isKo);

            cursorX += glyph.xAdvance * scale * glyph.spacingFactor + (GLYPH_SIZE*scale);
        }
    }

    private Glyph getGlyphForCharacter(char character) {
        return glyphs.get(character);  // 영어 및 기타 문자 처리
    }

    private void renderGlyph(Glyph glyph, Vector2f position, float scale, Texture texture, int VAO, boolean isKo) {
        int textureWidth = glyph.textSet.getWidth();
        int textureHeight = glyph.textSet.getHeight();

        // [🔵 수정된 코드] 한글과 영어의 texSize를 정확하게 계산
        Vector2f texSize = new Vector2f(
                (float) glyph.width / textureWidth,   // 가로 비율
                (float) glyph.height / textureHeight  // 세로 비율
        );

        // 기존 UV 좌표 계산 유지
        Vector2f texRegion = new Vector2f(glyph.xOffset, glyph.yOffset);

        // [📌 핵심 수정] 한글과 영어의 비율을 동일하게 유지
        Vector2f newScale = isKo ? new Vector2f(scale / (TEXTURE_WIDTH_KO / TEXTURE_WIDTH_EN), scale / (TEXTURE_HEIGHT_KO / TEXTURE_HEIGHT_EN)) : new Vector2f(scale, scale);

        TextureRenderer.getInstance().drawTexture(
                texture,
                texRegion,
                texSize,  // ✅ 올바르게 계산된 texSize 적용
                VAO,
                shaderProgram,
                position,
                newScale
        );
    }

    public void setScreenSize(int screenWidth,int screenHeight) {
        this.screenHeight = screenHeight;
        this.screenWidth = screenWidth;
    }

    public void cleanup() {
        glDeleteVertexArrays(VAO_EN);
        glDeleteBuffers(VBO_EN);
        glDeleteBuffers(EBO_EN);
        glDeleteVertexArrays(VAO_KO);
        glDeleteBuffers(VBO_KO);
        glDeleteBuffers(EBO_KO);
        for (Glyph i : glyphs.values()) {
            i.textSet.delete();
        }
    }
}