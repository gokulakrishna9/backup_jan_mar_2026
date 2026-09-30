package com.onlineshopping.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for storing complete deleted records as JSON.
 * Allows recovery and audit of deleted data.
 */
@Table("deleted_record")
public class DeletedRecord {
    
    @Id
    private Long id;
    
    @Column("entity_type")
    private String entityType;
    
    @Column("entity_id")
    private Long entityId;
    
    @Column("record_json")
    private String recordJson; // Complete JSON of deleted record
    
    @Column("deleted_by_user_id")
    private Long deletedByUserId;
    
    @Column("deleted_by_username")
    private String deletedByUsername;
    
    @Column("deleted_at")
    private LocalDateTime deletedAt;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("reason")
    private String reason;
    
    @Column("can_restore")
    private Boolean canRestore;
    
    // Constructors
    public DeletedRecord() {
        this.deletedAt = LocalDateTime.now();
        this.canRestore = true;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
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
    
    public String getRecordJson() {
        return recordJson;
    }
    
    public void setRecordJson(String recordJson) {
        this.recordJson = recordJson;
    }
    
    public Long getDeletedByUserId() {
        return deletedByUserId;
    }
    
    public void setDeletedByUserId(Long deletedByUserId) {
        this.deletedByUserId = deletedByUserId;
    }
    
    public String getDeletedByUsername() {
        return deletedByUsername;
    }
    
    public void setDeletedByUsername(String deletedByUsername) {
        this.deletedByUsername = deletedByUsername;
    }
    
    public LocalDateTime getDeletedAt() {
        return deletedAt;
    }
    
    public void setDeletedAt(LocalDateTime deletedAt) {
        this.deletedAt = deletedAt;
    }
    
    public String getIpAddress() {
        return ipAddress;
    }
    
    public void setIpAddress(String ipAddress) {
        this.ipAddress = ipAddress;
    }
    
    public String getReason() {
        return reason;
    }
    
    public void setReason(String reason) {
        this.reason = reason;
    }
    
    public Boolean getCanRestore() {
        return canRestore;
    }
    
    public void setCanRestore(Boolean canRestore) {
        this.canRestore = canRestore;
    }
}
