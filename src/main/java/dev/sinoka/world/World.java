package dev.sinoka.world;

import dev.sinoka.block.Block;
import dev.sinoka.model.Model;
import dev.sinoka.registry.BlockRegister;
import org.joml.Vector3f;
import org.joml.Vector3i;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class World {
    private final BlockRegister blockRegister;
    private final List<MapData> maps;

    public World() {
        this.blockRegister = new BlockRegister();
        this.maps = new ArrayList<>();
    }

    public void addMap(MapData map) {
        maps.add(map);
    }

    public void addBlockToMap(String mapName, int x, int y, int z, String blockID) {
        MapData map = getMap(mapName);
        if (map != null) {
            map.setBlockAt(x, y, z, blockID);
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
        System.out.println("🧹 Cleaning up world...");

        for (MapData map : maps) {
            for (String blockID : map.getTileMap().values()) {
                Block block = blockRegister.getBlock(blockID);
                if (block != null) {
                    block.delete();
                }
            }
        }

        System.out.println("✅ Cleanup complete.");
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

        System.out.println("🗺️ Map Contents - " + mapName + " 🗺️");
        map.getTileMap().forEach((position, blockID) ->
                System.out.println("📌 Block at " + position + " → " + blockID)
        );
        System.out.println("✅ End of map contents.");
    }
}
