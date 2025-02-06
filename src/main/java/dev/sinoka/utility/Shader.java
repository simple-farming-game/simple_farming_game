package dev.sinoka.utility;

import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;
import org.joml.Vector4f;
import org.lwjgl.opengl.GL20;
import org.lwjgl.system.MemoryStack;

import java.io.*;
import java.nio.file.*;
import static org.lwjgl.opengl.GL20.*;

public class Shader {
    private final int programId;

    public Shader(String vertexPath, String fragmentPath) {
        String vertexCode = readFile(vertexPath);
        String fragmentCode = readFile(fragmentPath);

        int vertexShader = compileShader(GL_VERTEX_SHADER, vertexCode);
        int fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentCode);

        programId = glCreateProgram();
        glAttachShader(programId, vertexShader);
        glAttachShader(programId, fragmentShader);
        glLinkProgram(programId);

        if (glGetProgrami(programId, GL_LINK_STATUS) == GL_FALSE) {
            throw new RuntimeException("Shader program linking failed: " + glGetProgramInfoLog(programId));
        }

        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);
    }

    public void use() {
        glUseProgram(programId);
    }

    public void setBool(String name, boolean value) {
        int location = glGetUniformLocation(programId, name);
        if (location == -1) {
            //System.err.println("Uniform '" + name + "' not found in shader!");
        } else {
            glUniform1i(location, value ? 1 : 0);
        }
    }

    public void setInt(String name, int value) {
        glUniform1i(glGetUniformLocation(programId, name), value);
    }

    public void setFloat(String name, float value) {
        glUniform1f(glGetUniformLocation(programId, name), value);
    }

    public void setVec2(String name, Vector2f velue) {
        int location = glGetUniformLocation(programId, name);
        glUniform2f(location, velue.x, velue.y);
    }

    public void setVec3(String name, Vector3f value) {
        glUniform3f(glGetUniformLocation(programId, name), value.x, value.y, value.z);
    }

    public void setVec4(String name, Vector4f value) {
        int location = glGetUniformLocation(programId, name);
        glUniform4f(location, value.x, value.y, value.z, value.w);
    }

    public void setMat4(String name, Matrix4f matrix) {
        try (MemoryStack stack = MemoryStack.stackPush()) {
            glUniformMatrix4fv(glGetUniformLocation(programId, name), false, matrix.get(stack.mallocFloat(16)));
        }
    }

    private int compileShader(int type, String code) {
        int shader = glCreateShader(type);
        glShaderSource(shader, code);
        glCompileShader(shader);

        if (glGetShaderi(shader, GL_COMPILE_STATUS) == GL_FALSE) {
            throw new RuntimeException("Shader compilation failed: " + glGetShaderInfoLog(shader));
        }

        return shader;
    }

    private String readFile(String path) {
        try {
            return new String(Files.readAllBytes(Paths.get(path)));
        } catch (IOException e) {
            throw new RuntimeException("Failed to read file: " + path, e);
        }
    }

    public void delete() {
        glDeleteProgram(programId);
    }
}