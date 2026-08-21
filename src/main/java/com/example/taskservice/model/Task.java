package com.example.taskservice.model;

/**
 * Represents a single to-do item exposed by the task service.
 *
 * @param id        unique identifier of the task
 * @param title     human-readable description of the task
 * @param completed whether the task has already been done
 */
public record Task(Long id, String title, boolean completed) {
}
