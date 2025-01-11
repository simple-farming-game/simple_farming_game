package dev.sinoka.utility;

import org.joml.*;
import org.joml.Math;

public class Camera {
    public enum Movement {
        FORWARD, BACKWARD, LEFT, RIGHT
    }

    private Vector3f position;
    private Vector3f front;
    private Vector3f up;
    private Vector3f right;
    private Vector3f worldUp;

    private float yaw;
    private float pitch;

    private float movementSpeed;
    private float mouseSensitivity;
    private float zoom;

    public Camera(Vector3f position) {
        this.position = position;
        this.front = new Vector3f(0.0f, 0.0f, -1.0f);
        this.worldUp = new Vector3f(0.0f, 1.0f, 0.0f);
        this.yaw = -90.0f;
        this.pitch = 0.0f;
        this.movementSpeed = 2.5f;
        this.mouseSensitivity = 0.1f;
        this.zoom = 45.0f;
        updateCameraVectors();
    }

    public Matrix4f getViewMatrix() {
        return new Matrix4f().lookAt(position, new Vector3f(position).add(front), up);
    }

    public void processKeyboard(Movement direction, float deltaTime) {
        float velocity = movementSpeed * deltaTime;
        if (direction == Movement.FORWARD) {
            position.add(new Vector3f(front).mul(velocity));
        } else if (direction == Movement.BACKWARD) {
            position.sub(new Vector3f(front).mul(velocity));
        } else if (direction == Movement.LEFT) {
            position.sub(new Vector3f(right).mul(velocity));
        } else if (direction == Movement.RIGHT) {
            position.add(new Vector3f(right).mul(velocity));
        }
    }

    public void processMouseMovement(float xoffset, float yoffset, boolean constrainPitch) {
        xoffset *= mouseSensitivity;
        yoffset *= mouseSensitivity;

        yaw += xoffset;
        pitch += yoffset;

        if (constrainPitch) {
            if (pitch > 89.0f) {
                pitch = 89.0f;
            }
            if (pitch < -89.0f) {
                pitch = -89.0f;
            }
        }

        updateCameraVectors();
    }

    public void processMouseScroll(float yoffset) {
        zoom -= yoffset;
        if (zoom < 1.0f) {
            zoom = 1.0f;
        }
        if (zoom > 45.0f) {
            zoom = 45.0f;
        }
    }

    public float getZoom() {
        return zoom;
    }

    public Vector3f getPosition() {
        return position;
    }

    private void updateCameraVectors() {
        Vector3f newFront = new Vector3f();
        newFront.x = (float) Math.cos(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
        newFront.y = (float) Math.sin(Math.toRadians(pitch));
        newFront.z = (float) Math.sin(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
        front.set(newFront).normalize();

        right = new Vector3f(front).cross(worldUp).normalize();
        up = new Vector3f(right).cross(front).normalize();
    }
}