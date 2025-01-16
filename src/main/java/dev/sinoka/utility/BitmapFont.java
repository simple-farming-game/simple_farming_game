package dev.sinoka.utility;

import org.joml.Vector2f;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

import static org.lwjgl.opengl.GL11.GL_TEXTURE_2D;
import static org.lwjgl.opengl.GL11.glBindTexture;
import static org.lwjgl.opengl.GL13.*;

public class BitmapFont {
    private static final int TEXTURE_SIZE = 100;
    private static final int GLYPH_SIZE = 10;
    private static final int GLYPH_COLUMNS = 10;
    private static final int GLYPH_ROWS = 10;

    private final int VAO;
    private final int textureID;
    private final Shader shaderProgram;
    private int screenWidth;
    private int screenHeight;

    private float defaultSpacingFactor = 1.0f;
    private Map<Character, Glyph> glyphs = new HashMap<>();

    static class Glyph {
        int textSetID;
        int width, height;
        float xOffset, yOffset;
        float xAdvance;
        float spacingFactor;

        public Glyph(int textTextureID, Vector2f glyphSize, float xOffset, float yOffset, float xAdvance, float spacingFactor) {
            this.textSetID = textTextureID;
            this.width = (int) glyphSize.x;
            this.height = (int) glyphSize.y;
            this.xOffset = xOffset;
            this.yOffset = yOffset;
            this.xAdvance = xAdvance;
            this.spacingFactor = spacingFactor;
        }
    }

    public BitmapFont(int VAO, int textureID, Shader shaderProgram, JsonFileReader JFR, int screenWidth, int screenHeight) {
        this.VAO = VAO;
        this.textureID = textureID;
        this.shaderProgram = shaderProgram;
        this.screenWidth = screenWidth;
        this.screenHeight = screenHeight;

        JSONObject fontData = JFR.readJson();
        if (fontData != null) {
            if (fontData.has("default")) {
                this.defaultSpacingFactor = (float) fontData.getDouble("default");
            }

            if (fontData.has("glyphs")) {
                JSONObject glyphData = fontData.getJSONObject("glyphs");

                for (int i = 0; i < 95; i++) { // ASCII 32 (' ') ~ 126 ('~')
                    char character = (char) (i + 32);

                    // 글자에 대한 개별 설정이 존재하면 읽어오기
                    float spacingFactor = glyphData.has(Character.toString(character))
                            ? (float) glyphData.optDouble(Character.toString(character), defaultSpacingFactor)
                            : defaultSpacingFactor;

                    int glyphX = i % GLYPH_COLUMNS;
                    int glyphY = i / GLYPH_COLUMNS;
                    Vector2f glyphSize = new Vector2f(GLYPH_SIZE, GLYPH_SIZE);
                    float xOffset = (1f / GLYPH_COLUMNS) * glyphX;
                    float yOffset = 1f - ((1f / GLYPH_ROWS) * (glyphY + 1));
                    float xAdvance = GLYPH_SIZE;

                    glyphs.put(character, new Glyph(textureID, glyphSize, xOffset, yOffset, xAdvance, spacingFactor));
                }
            }
        }
    }

    public void renderString(String text, Vector2f position, float scale) {
        float cursorX = position.x;
        float cursorY = position.y;

        for (char c : text.toCharArray()) {
            if (!glyphs.containsKey(c)) continue;

            Glyph glyph = glyphs.get(c);
            renderGlyph(glyph, new Vector2f(cursorX, cursorY), scale);

            cursorX += glyph.xAdvance * scale * glyph.spacingFactor;
        }
    }

    private void renderGlyph(Glyph glyph, Vector2f position, float scale) {
        Vector2f texRegion = new Vector2f(
                glyph.xOffset,
                glyph.yOffset
        );

        Vector2f texSize = new Vector2f(
                glyph.width / (float) TEXTURE_SIZE,
                glyph.height / (float) TEXTURE_SIZE
        );

        glActiveTexture(GL_TEXTURE1);
        glBindTexture(GL_TEXTURE_2D, glyph.textSetID);

        Renderer.drawTexture(
                1,
                texRegion,
                texSize,
                VAO,
                shaderProgram,
                position,
                scale
        );
    }

    public void setScreenSize(Vector2f size) {
        this.screenWidth = (int) size.x;
        this.screenHeight = (int) size.y;
    }
}
