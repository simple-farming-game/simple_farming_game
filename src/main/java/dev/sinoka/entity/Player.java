package dev.sinoka.entity;

import org.joml.Vector3f;

public class Player {
    private Vector3f pos;
    private Vector3f velocity;
    private BoxCollision collision;

    public Player(Vector3f pos) {
        this.pos = pos;
        Vector3f size = new Vector3f(1,2,0.5f);
        this.collision = new BoxCollision(pos.sub(size.x*0.5f,0,0), size);
        this.velocity = new Vector3f(0, 0, 0); // 초기 속도 0으로 설정
        collision.setSolid(true);
    }

    public Vector3f getPos() {
        return pos;
    }

    public void setPos(Vector3f pos) {
        this.pos = pos;
        collision.setPosition(pos);
    }

    public Vector3f getVelocity() {
        return velocity;
    }

    public void setVelocity(Vector3f velocity) {
        this.velocity = velocity;
    }

    public BoxCollision getCollision() {
        return collision;
    }
}
