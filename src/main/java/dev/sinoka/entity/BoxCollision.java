package dev.sinoka.entity;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.joml.Vector3f;

public class BoxCollision {
    private Vector3f position; // 객체의 위치
    private Vector3f size;     // 충돌 박스의 크기
    private boolean isSolid;   // 충돌 가능한지 여부
    private static final Logger logger = LogManager.getLogger(BoxCollision.class);

    public BoxCollision(Vector3f position, Vector3f size) {
        this.position = position;
        this.size = size;
        this.isSolid = true; // 기본값
    }

    public boolean intersects(BoxCollision other) {
        if (!this.isSolid || !other.isSolid) {
            return false; // 둘 중 하나라도 비단단한 경우 충돌하지 않음
        }

        // AABB 충돌 검사 (축 정렬된 방식)
        boolean overlapX = this.position.x + this.size.x / 2 > other.position.x - other.size.x / 2 &&
                this.position.x - this.size.x / 2 < other.position.x + other.size.x / 2;

        boolean overlapY = this.position.y + this.size.y / 2 > other.position.y - other.size.y / 2 &&
                this.position.y - this.size.y / 2 < other.position.y + other.size.y / 2;

        boolean overlapZ = this.position.z + this.size.z / 2 > other.position.z - other.size.z / 2 &&
                this.position.z - this.size.z / 2 < other.position.z + other.size.z / 2;

        // X, Y, Z 축 모두 겹치면 충돌
        return overlapX && overlapY && overlapZ;
    }



    public boolean intersects(CompoundCollision compoundCollision) {
        // CompoundCollision 내의 각 BoxCollision과 현재 BoxCollision 간의 충돌 검사
        for (BoxCollision otherBox : compoundCollision.getBoxCollisions()) {
            if (this.intersects(otherBox)) {
                return true;
            }
        }
        return false;
    }

    public boolean isPointInside(Vector3f point) {
        return (point.x >= position.x - size.x / 2 && point.x <= position.x + size.x / 2 &&
                point.y >= position.y - size.y / 2 && point.y <= position.y + size.y / 2 &&
                point.z >= position.z - size.z / 2 && point.z <= position.z + size.z / 2);
    }

    public Vector3f getPosition() {
        return position;
    }

    public Vector3f getSize() {
        return size;
    }

    public boolean isSolid() {
        return isSolid;
    }

    public void setPosition(Vector3f position) {
        this.position = position;
    }

    public void setSize(Vector3f size) {
        this.size = size;
    }

    public void setSolid(boolean solid) {
        isSolid = solid;
    }
}
