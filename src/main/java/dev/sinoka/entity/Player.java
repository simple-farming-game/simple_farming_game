package dev.sinoka.entity;

import dev.sinoka.block.Block;
import dev.sinoka.utility.Camera;
import dev.sinoka.world.World;
import org.joml.Vector3f;

public class Player {
    private Vector3f pos;
    private Vector3f velocity;
    private BoxCollision collision;
    private int dist = 10;

    public Player(Vector3f pos) {
        this.pos = pos;
        Vector3f size = new Vector3f(0.5f, 2, 0);
        this.collision = new BoxCollision(pos.sub(size.x * 0.5f, 0, size.z * 0.5f), size);
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

    public void rotateProcess(Camera camera) {
        collision.rotate(camera.getYaw());
    }

    public Block getSelectBlock(World world, Camera camera, String mapName){
        boolean isSelect;
        Vector3f selectPos = new Vector3f(camera.getPosition()); // 카메라의 위치를 복사
        Block selectBlock;

        for (int i = 0; i < dist; i++) {
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

        for (int i = 0; i < dist; i++) {
            selectBlock = world.getBlockAt(selectPos);
            isSelect = world.getCompoundCollision(mapName).isPointInside(selectPos);

            if (isSelect) {
                return selectPos;
            }

            selectPos.add(camera.getDirectionVector());
        }
        return null;
    }

    public Vector3f getSelectBlockFace(World world, Camera camera, String mapName) {
        // 카메라 위치에서 ray 시작 (현재 위치와 이전 위치를 기록)
        Vector3f currentPos = new Vector3f(camera.getPosition());
        Vector3f prevPos = new Vector3f(currentPos);
        // 카메라가 바라보는 단위벡터 (ray 방향)
        Vector3f direction = new Vector3f(camera.getDirectionVector());

        // 최대 탐색 거리 (예를 들어, dist 변수로 정해짐)
        for (int i = 0; i < dist; i++) {
            // 이전 위치 업데이트
            prevPos.set(currentPos);
            // 한 스텝씩 ray 진행
            currentPos.add(direction);

            // 현재 위치가 지정한 충돌 영역(예: 맵의 블록 충돌 영역)에 들어갔는지 체크
            if (world.getCompoundCollision(mapName).isPointInside(currentPos)) {
                // currentPos가 들어있는 블록의 좌표 (단위 큐브이므로, floor()를 사용)
                int blockX = (int) Math.floor(currentPos.x);
                int blockY = (int) Math.floor(currentPos.y);
                int blockZ = (int) Math.floor(currentPos.z);

                // 충돌한 면을 나타낼 단위 벡터 (노멀)
                Vector3f faceNormal = new Vector3f();

                /*
                 * prevPos는 블록 외부에 있었으므로, prevPos와 블록 경계를 비교하여 어느 면으로 들어왔는지 결정합니다.
                 * 각 좌표별로 블록의 최소/최대값과 비교합니다.
                 */
                if (prevPos.x < blockX) {
                    faceNormal.set(-1, 0, 0); // 왼쪽 면(-X)
                } else if (prevPos.x >= blockX + 1) {
                    faceNormal.set(1, 0, 0);  // 오른쪽 면(+X)
                } else if (prevPos.y < blockY) {
                    faceNormal.set(0, -1, 0); // 아래쪽 면(-Y)
                } else if (prevPos.y >= blockY + 1) {
                    faceNormal.set(0, 1, 0);  // 위쪽 면(+Y)
                } else if (prevPos.z < blockZ) {
                    faceNormal.set(0, 0, -1); // 뒤쪽 면(-Z)
                } else if (prevPos.z >= blockZ + 1) {
                    faceNormal.set(0, 0, 1);  // 앞쪽 면(+Z)
                }
                return faceNormal;
            }
        }
        // 충돌한 블록이 없으면 null 리턴
        return null;
    }


    public void blockBreakProcess(World world, String mapName, Vector3f pos) {
        world.removeBlockFromMap(mapName, (int) pos.x, (int) pos.y, (int) pos.z);
    }

    /**
     * 플레이어가 바라보는 블록의 방향을 계산하여 블록을 배치하는 함수
     */
    public void blockPlaceProcess(World world, String mapName, Camera camera, Vector3f pos, String blockID) {

        Vector3f blockPos = new Vector3f(pos).add(getSelectBlockFace(world, camera, mapName));

        world.addBlockToMap(mapName, (int) blockPos.x,(int) blockPos.y,(int) blockPos.z, blockID);
    }
}
