package dev.sinoka.input;

import static org.lwjgl.glfw.GLFW.*;
import java.util.HashMap;
import java.util.Map;

public class InputManager {
    private final long window;
    private final Map<Integer, Boolean> previousKeyState = new HashMap<>();
    private final Map<Integer, Boolean> currentKeyState = new HashMap<>();
    private final Map<Integer, Boolean> previousMouseState = new HashMap<>();
    private final Map<Integer, Boolean> currentMouseState = new HashMap<>();

    private static final int[] TRACKED_KEYS = {
            GLFW_KEY_W, GLFW_KEY_A, GLFW_KEY_S, GLFW_KEY_D,
            GLFW_KEY_SPACE, GLFW_KEY_ESCAPE, GLFW_KEY_R
    };

    private static final int[] TRACKED_MOUSE_BUTTONS = {
            GLFW_MOUSE_BUTTON_LEFT, GLFW_MOUSE_BUTTON_RIGHT
    };

    public InputManager(long window) {
        this.window = window;
    }

    public void update() {
        // ✅ 키 상태 업데이트
        for (int key : TRACKED_KEYS) {
            boolean isPressed = glfwGetKey(window, key) == GLFW_PRESS;
            previousKeyState.put(key, currentKeyState.getOrDefault(key, false));
            currentKeyState.put(key, isPressed);
        }

        // ✅ 마우스 상태 업데이트
        for (int button : TRACKED_MOUSE_BUTTONS) {
            boolean isPressed = glfwGetMouseButton(window, button) == GLFW_PRESS;
            previousMouseState.put(button, currentMouseState.getOrDefault(button, false));
            currentMouseState.put(button, isPressed);
        }
    }

    // ✅ 키가 눌려있는지 확인 (계속 활성화됨)
    public boolean isKeyHeld(int key) {
        return currentKeyState.getOrDefault(key, false);
    }

    // ✅ 키가 눌린 순간만 감지 (한 번만 활성화)
    public boolean isKeyPressed(int key) {
        return currentKeyState.getOrDefault(key, false) && !previousKeyState.getOrDefault(key, false);
    }

    // ✅ 마우스 버튼이 눌린 순간만 감지
    public boolean isMouseButtonPressed(int button) {
        return currentMouseState.getOrDefault(button, false) && !previousMouseState.getOrDefault(button, false);
    }

    // ✅ 마우스 버튼이 유지되는지 확인
    public boolean isMouseButtonHeld(int button) {
        return currentMouseState.getOrDefault(button, false);
    }
}
