package dev.sinoka.entity;

import dev.sinoka.block.Block;
import dev.sinoka.utility.Camera;
import dev.sinoka.world.World;
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

    public Block getSelectBlock(World world, Camera camera, String mapName){
        boolean isSelect;
        Vector3f selectPos = new Vector3f(camera.getPosition()); // 카메라의 위치를 복사
        Block selectBlock;

        for (int i = 0; i < 10; i++) {
            selectBlock = world.getBlockAt(selectPos);
            isSelect = world.getCompoundCollision(mapName).isPointInside(selectPos);

            if (isSelect) {
                return selectBlock;
            }

            selectPos.add(camera.getDirectionVector());
        }
        return null;
    }

    public Vector3f getSelectBlockPos(World world, Camera camera, String mapName){
        boolean isSelect;
        Vector3f selectPos = new Vector3f(camera.getPosition()); // 카메라의 위치를 복사
        Block selectBlock;

        for (int i = 0; i < 10; i++) {
            selectBlock = world.getBlockAt(selectPos);
            isSelect = world.getCompoundCollision(mapName).isPointInside(selectPos);

            if (isSelect) {
                return selectPos;
            }

            selectPos.add(camera.getDirectionVector());
        }
        return null;
    }
}
