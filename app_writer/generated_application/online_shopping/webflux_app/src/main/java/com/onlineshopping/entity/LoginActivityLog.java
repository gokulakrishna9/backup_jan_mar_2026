package com.onlineshopping.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for tracking user login and logout activities.
 * Records authentication events with session information.
 */
@Table("login_activity_log")
public class LoginActivityLog {
    
    @Id
    private Long id;
    
    @Column("user_id")
    private Long userId;
    
    @Column("username")
    private String username;
    
    @Column("activity_type")
    private String activityType; // LOGIN, LOGOUT, LOGIN_FAILED
    
    @Column("timestamp")
    private LocalDateTime timestamp;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("user_agent")
    private String userAgent;
    
    @Column("session_id")
    private String sessionId;
    
    @Column("success")
    private Boolean success;
    
    @Column("failure_reason")
    private String failureReason;
    
    @Column("login_method")
    private String loginMethod; // PASSWORD, OAUTH2, SAML
    
    @Column("oauth2_provider")
    private String oauth2Provider; // Google, GitHub, etc.
    
    // Constructors
    public LoginActivityLog() {
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
    
    public String getActivityType() {
        return activityType;
    }
    
    public void setActivityType(String activityType) {
        this.activityType = activityType;
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
    
    public String getSessionId() {
        return sessionId;
    }
    
    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }
    
    public Boolean getSuccess() {
        return success;
    }
    
    public void setSuccess(Boolean success) {
        this.success = success;
    }
    
    public String getFailureReason() {
        return failureReason;
    }
    
    public void setFailureReason(String failureReason) {
        this.failureReason = failureReason;
    }
    
    public String getLoginMethod() {
        return loginMethod;
    }
    
    public void setLoginMethod(String loginMethod) {
        this.loginMethod = loginMethod;
    }
    
    public String getOauth2Provider() {
        return oauth2Provider;
    }
    
    public void setOauth2Provider(String oauth2Provider) {
        this.oauth2Provider = oauth2Provider;
    }
}
