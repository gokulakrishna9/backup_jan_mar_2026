package com.onlineshopping.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for tracking CRUD operations on all entities.
 * Records create, read, update, and delete operations with full context.
 */
@Table("crud_activity_log")
public class CrudActivityLog {
    
    @Id
    private Long id;
    
    @Column("user_id")
    private Long userId;
    
    @Column("username")
    private String username;
    
    @Column("entity_type")
    private String entityType;
    
    @Column("entity_id")
    private Long entityId;
    
    @Column("operation")
    private String operation; // CREATE, READ, UPDATE, DELETE
    
    @Column("timestamp")
    private LocalDateTime timestamp;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("user_agent")
    private String userAgent;
    
    @Column("changes_json")
    private String changesJson; // JSON of what changed (for UPDATE)
    
    @Column("success")
    private Boolean success;
    
    @Column("error_message")
    private String errorMessage;
    
    // Constructors
    public CrudActivityLog() {
        this.timestamp = LocalDateTime.now();
        this.success = true;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Long getUserId() {
        return userId;
    }
    
    public void setUserId(Long userId) {
        this.userId = userId;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public String getEntityType() {
        return entityType;
    }
    
    public void setEntityType(String entityType) {
        this.entityType = entityType;
    }
    
    public Long getEntityId() {
        return entityId;
    }
    
    public void setEntityId(Long entityId) {
        this.entityId = entityId;
    }
    
    public String getOperation() {
        return operation;
    }
    
    public void setOperation(String operation) {
        this.operation = operation;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
    public String getIpAddress() {
        return ipAddress;
    }
    
    public void setIpAddress(String ipAddress) {
        this.ipAddress = ipAddress;
    }
    
    public String getUserAgent() {
        return userAgent;
    }
    
    public void setUserAgent(String userAgent) {
        this.userAgent = userAgent;
    }
    
    public String getChangesJson() {
        return changesJson;
    }
    
    public void setChangesJson(String changesJson) {
        this.changesJson = changesJson;
    }
    
    public Boolean getSuccess() {
        return success;
    }
    
    public void setSuccess(Boolean success) {
        this.success = success;
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
