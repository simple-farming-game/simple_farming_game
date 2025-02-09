package dev.sinoka.world;

import dev.sinoka.block.Block;
import dev.sinoka.entity.BoxCollision;
import dev.sinoka.entity.CompoundCollision;
import dev.sinoka.model.Model;
import dev.sinoka.registry.BlockRegister;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.joml.Vector3f;
import org.joml.Vector3i;

import java.lang.reflect.WildcardType;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class World {
    private final BlockRegister blockRegister;
    private final List<MapData> maps;
    private List<CompoundCollision> compoundCollisions; // 각 맵에 대한 컴파운드 콜리전 캐싱
    private List<Boolean> mapChangedFlags = new ArrayList<>();
    private static final Logger logger = LogManager.getLogger(World.class);

    public World() {
        this.blockRegister = new BlockRegister();
        this.maps = new ArrayList<>();
        this.compoundCollisions = new ArrayList<>();
        this.mapChangedFlags = new ArrayList<>();
    }

    public void addMap(MapData map) {
        maps.add(map);
        logger.debug("Added map: " + map.getMapName());  // 디버깅용 출력
        compoundCollisions.add(null); // 빈 값 추가
        mapChangedFlags.add(true);   // 기본값은 false
    }

    public void addBlockToMap(String mapName, int x, int y, int z, String blockID) {
        MapData map = getMap(mapName);
        if (map != null) {
            map.setBlockAt(x, y, z, blockID);
            setMapChanged(maps.indexOf(map));  // ✅ 맵이 변경됨을 표시
        } else {
            System.err.println("❌ Map '" + mapName + "' not found!");
        }
    }

    public void removeBlockFromMap(String mapName, int x, int y, int z) {
        MapData map = getMap(mapName);
        if (map != null) {
            map.removeBlockAt(x, y, z);
            setMapChanged(maps.indexOf(map));  // ✅ 맵이 변경됨을 표시
        } else {
            System.err.println("❌ Map '" + mapName + "' not found!");
        }
    }


    public void render(String mapName) {
        MapData map = getMap(mapName);
        if (map == null) {
            System.err.println("❌ Map '" + mapName + "' not found!");
            return;
        }

        for (Map.Entry<Vector3i, String> entry : map.getTileMap().entrySet()) {
            Block block = blockRegister.getBlock(entry.getValue());
            if (block != null) {
                Vector3i position = entry.getKey();
                Vector3f worldPos = new Vector3f(position).mul(block.getBlockSize());
                block.render(worldPos);
            }
        }
    }

    public BlockRegister getBlockRegister() {
        return blockRegister;
    }

    /**
     * 📌 **블록의 실제 크기를 고려한 위치 반환**
     */
    public List<Vector3f> getBlockPositions() {
        List<Vector3f> positions = new ArrayList<>();
        for (MapData map : maps) {
            for (Map.Entry<Vector3i, String> entry : map.getTileMap().entrySet()) {
                Block block = blockRegister.getBlock(entry.getValue());
                if (block != null) {
                    Vector3f blockPos = new Vector3f(entry.getKey()).mul(block.getBlockSize());
                    positions.add(blockPos);
                }
            }
        }
        return positions;
    }

    /**
     * 📌 **블록의 위치 기반으로 블록 가져오기 (충돌 감지에 활용)**
     * - 플레이어 위치에 해당하는 블록이 존재하면 반환
     * - 없으면 `null`
     */
    public Block getBlockAt(Vector3f position) {
        for (MapData map : maps) {
            for (Map.Entry<Vector3i, String> entry : map.getTileMap().entrySet()) {
                Block block = blockRegister.getBlock(entry.getValue());
                if (block == null) continue;

                float blockSize = block.getBlockSize();
                Vector3f blockPos = new Vector3f(entry.getKey()).mul(blockSize);

                // 블록의 AABB 범위 (왼쪽 아래 뒷부분 기준 적용)
                float minX = blockPos.x;               // 왼쪽
                float maxX = minX + blockSize;         // 오른쪽
                float minY = blockPos.y;               // 아래쪽 (변경됨)
                float maxY = blockPos.y + blockSize;   // 위쪽 (변경됨)
                float minZ = blockPos.z;               // 뒤쪽
                float maxZ = blockPos.z + blockSize;   // 앞쪽

                // 플레이어 위치가 블록 범위 내에 있는지 확인
                boolean withinX = position.x >= minX && position.x <= maxX;
                boolean withinY = position.y >= minY && position.y <= maxY;
                boolean withinZ = position.z >= minZ && position.z <= maxZ;

                if (withinX && withinY && withinZ) {
                    return block;
                }
            }
        }
        return null;
    }

    public void cleanup() {
        logger.debug("🧹 Cleaning up world...");

        for (MapData map : maps) {
            for (String blockID : map.getTileMap().values()) {
                Block block = blockRegister.getBlock(blockID);
                if (block != null) {
                    block.delete();
                }
            }
        }

        logger.debug("✅ Cleanup complete.");
    }

    public List<MapData> getMaps() {
        return new ArrayList<>(maps);
    }

    public MapData getMap(String mapName) {
        return maps.stream()
                .filter(map -> map.getMapName().equals(mapName))
                .findFirst()
                .orElse(null);
    }

    public void printMapContents(String mapName) {
        MapData map = getMap(mapName);
        if (map == null) {
            System.err.println("❌ Map '" + mapName + "' not found!");
            return;
        }

        logger.debug("🗺️ Map Contents - " + mapName + " 🗺️");
        map.getTileMap().forEach((position, blockID) ->
                logger.debug("📌 Block at " + position + " → " + blockID)
        );
        logger.debug("✅ End of map contents.");
    }

    public CompoundCollision getCompoundCollision(String mapName) {
        MapData map = getMap(mapName);
        if (map == null) {
            System.err.println("❌ Map '" + mapName + "' not found!");
            return null;
        }

        int mapIndex = maps.indexOf(map);
        if (mapIndex == -1) {
            System.err.println("❌ Map '" + mapName + "' not found in list!");
            return null;
        }

        // 맵이 변경되었으면 콜리전 객체를 새로 생성
        if (mapChangedFlags.get(mapIndex)) {
            List<BoxCollision> boxCollisions = new ArrayList<>();

            for (Map.Entry<Vector3i, String> entry : map.getTileMap().entrySet()) {
                Block block = blockRegister.getBlock(entry.getValue());
                if (block != null && block.isSolid()) {
                    Vector3i position = entry.getKey();
                    float blockSize = block.getBlockSize();
                    Vector3f worldPos = new Vector3f(position).mul(blockSize);
                    Vector3f size = new Vector3f(blockSize, blockSize, blockSize); // AABB 크기 설정

                    // 박스를 콜리전 목록에 추가
                    BoxCollision box = new BoxCollision(worldPos, size);
                    boxCollisions.add(box);
                }
            }

            // 새로운 CompoundCollision 객체를 생성하여 저장
            CompoundCollision newCompoundCollision = new CompoundCollision(boxCollisions);
            compoundCollisions.set(mapIndex, newCompoundCollision); // 기존 콜리전 업데이트
            mapChangedFlags.set(mapIndex, false); // 콜리전 객체가 생성된 후 상태를 false로 변경
            return newCompoundCollision;
        } else {
            // 변경되지 않았으면 기존 콜리전 객체 반환
            return compoundCollisions.get(mapIndex);
        }
    }


    // 맵 변경 상태에 맞게 compoundCollisions와 mapChangedFlags 크기를 맞추는 메서드
    private void ensureCompoundCollisionSize(int mapIndex) {
        // compoundCollisions 크기 맞추기
        while (compoundCollisions.size() <= mapIndex) {
            compoundCollisions.add(null); // 부족한 크기만큼 null 추가
        }

        // mapChangedFlags 크기 맞추기
        while (mapChangedFlags.size() <= mapIndex) {
            mapChangedFlags.add(false); // 부족한 크기만큼 false 추가
        }
    }

    /**
     * 📌 **맵 변경 시 콜리전 객체를 새로 생성하도록 설정**
     * - 맵에 블록을 추가하거나 삭제할 때 호출
     */
    public void setMapChanged(int mapIndex) {
        if (mapIndex >= 0 && mapIndex < mapChangedFlags.size()) {
            mapChangedFlags.set(mapIndex, true);  // 맵이 변경되었음을 표시
        } else {
            System.err.println("❌ Invalid map index: " + mapIndex);
        }
    }
}
