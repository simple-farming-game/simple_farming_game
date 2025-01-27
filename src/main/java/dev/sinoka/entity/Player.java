package dev.sinoka.entity;

import dev.sinoka.utility.Camera;
import org.joml.Vector3f;

public class Player {
    private Vector3f pos;
    private Vector3f velocity;

    public Player(Vector3f pos) {
        this.pos = pos;
        this.velocity = new Vector3f(0, 0, 0); // 초기 속도 0으로 설정
    }

    public Vector3f getPos() {
        return pos;
    }

    public void setPos(Vector3f pos) {
        this.pos = pos;
    }

    public Vector3f getVelocity() {
        return velocity;
    }

    public void setVelocity(Vector3f velocity) {
        this.velocity = velocity;
    }
}
