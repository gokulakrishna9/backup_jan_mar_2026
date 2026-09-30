package com.example.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for tracking permission and grant changes.
 * Records all authorization modifications including group memberships and access controls.
 */
@Table("grant_activity_log")
public class GrantActivityLog {
    
    @Id
    private Long id;
    
    @Column("granted_by_user_id")
    private Long grantedByUserId;
    
    @Column("granted_by_username")
    private String grantedByUsername;
    
    @Column("target_user_id")
    private Long targetUserId;
    
    @Column("target_username")
    private String targetUsername;
    
    @Column("grant_type")
    private String grantType; // GROUP_MEMBERSHIP, ACCESS_CONTROL, DOCUMENT_PERMISSION, ROLE_CHANGE
    
    @Column("action")
    private String action; // GRANT, REVOKE, MODIFY
    
    @Column("entity_type")
    private String entityType; // UserGroup, AccessControl, DocumentPermission, etc.
    
    @Column("entity_id")
    private Long entityId;
    
    @Column("previous_value_json")
    private String previousValueJson;
    
    @Column("new_value_json")
    private String newValueJson;
    
    @Column("timestamp")
    private LocalDateTime timestamp;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("reason")
    private String reason;
    
    // Constructors
    public GrantActivityLog() {
        this.timestamp = LocalDateTime.now();
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public Long getGrantedByUserId() {
        return grantedByUserId;
    }
    
    public void setGrantedByUserId(Long grantedByUserId) {
        this.grantedByUserId = grantedByUserId;
    }
    
    public String getGrantedByUsername() {
        return grantedByUsername;
    }
    
    public void setGrantedByUsername(String grantedByUsername) {
        this.grantedByUsername = grantedByUsername;
    }
    
    public Long getTargetUserId() {
        return targetUserId;
    }
    
    public void setTargetUserId(Long targetUserId) {
        this.targetUserId = targetUserId;
    }
    
    public String getTargetUsername() {
        return targetUsername;
    }
    
    public void setTargetUsername(String targetUsername) {
        this.targetUsername = targetUsername;
    }
    
    public String getGrantType() {
        return grantType;
    }
    
    public void setGrantType(String grantType) {
        this.grantType = grantType;
    }
    
    public String getAction() {
        return action;
    }
    
    public void setAction(String action) {
        this.action = action;
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
    
    public String getPreviousValueJson() {
        return previousValueJson;
    }
    
    public void setPreviousValueJson(String previousValueJson) {
        this.previousValueJson = previousValueJson;
    }
    
    public String getNewValueJson() {
        return newValueJson;
    }
    
    public void setNewValueJson(String newValueJson) {
        this.newValueJson = newValueJson;
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
    
    public String getReason() {
        return reason;
    }
    
    public void setReason(String reason) {
        this.reason = reason;
    }
}
