package com.example.taskservice.controller;

import com.example.taskservice.model.Task;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Exposes a read-only REST endpoint that returns the current list of tasks.
 */
@RestController
public class TaskController {

    private final List<Task> tasks = List.of(
            new Task(1L, "Изучить Spring Boot", false),
            new Task(2L, "Настроить CI/CD", false),
            new Task(3L, "Написать тесты", true)
    );

    /**
     * Returns the full list of tasks.
     *
     * @return list of {@link Task} objects
     */
    @GetMapping("/api/tasks")
    public List<Task> getTasks() {
        return tasks;
    }
}
