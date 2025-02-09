package dev.sinoka.world;

import org.joml.Vector3i;
import java.util.HashMap;
import java.util.Map;

public class MapData {
    private final String mapName;
    private final Map<Vector3i, String> tileMap; // 위치(타일 좌표) → 블록 ID

    public MapData(String mapName) {
        this.mapName = mapName;
        this.tileMap = new HashMap<>();
    }

    public void setBlockAt(int x, int y, int z, String blockID) {
        Vector3i position = new Vector3i(x, y, z);
        // 기존에 블록이 있으면 덮어쓰기
        if (tileMap.containsKey(position)) {
            tileMap.remove(position);
        }
        tileMap.put(position, blockID);
    }

    public void removeBlockAt(int x, int y, int z) {
        Vector3i position = new Vector3i(x, y, z);
        // 해당 위치에 블록이 있으면 제거
        if (tileMap.containsKey(position)) {
            tileMap.remove(position);
        }
    }

    public String getBlockAt(int x, int y, int z) {
        return tileMap.getOrDefault(new Vector3i(x, y, z), "air"); // 기본값: air (빈 공간)
    }

    public boolean hasBlockAt(int x, int y, int z) {
        return tileMap.containsKey(new Vector3i(x, y, z));
    }

    public String getMapName() {
        return mapName;
    }

    public Map<Vector3i, String> getTileMap() {
        return tileMap;
    }
}
