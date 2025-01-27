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
        tileMap.put(new Vector3i(x, y, z), blockID);
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
