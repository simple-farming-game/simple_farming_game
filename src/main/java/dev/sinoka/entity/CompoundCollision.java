package dev.sinoka.entity;

import org.joml.Vector3f;
import java.util.List;

public class CompoundCollision {
    private List<BoxCollision> boxCollisions;

    public CompoundCollision(List<BoxCollision> boxCollisions) {
        this.boxCollisions = boxCollisions;
    }

    public boolean intersects(CompoundCollision other) {
        for (BoxCollision thisBox : boxCollisions) {
            for (BoxCollision otherBox : other.boxCollisions) {
                if (thisBox.intersects(otherBox)) {
                    return true;
                }
            }
        }
        return false;
    }

    public boolean intersects(BoxCollision box) {
        // CompoundCollision 내 모든 BoxCollision과 현재 박스 간의 충돌을 검사
        for (BoxCollision thisBox : boxCollisions) {
            if (thisBox.intersects(box)) {
                return true;
            }
        }
        return false;
    }

    public boolean isPointInside(Vector3f point) {
        for (BoxCollision box : boxCollisions) {
            if (box.isPointInside(point)) {
                return true;
            }
        }
        return false;
    }

    public List<BoxCollision> getBoxCollisions() {
        return boxCollisions;
    }

    public void setBoxCollisions(List<BoxCollision> boxCollisions) {
        this.boxCollisions = boxCollisions;
    }
}
