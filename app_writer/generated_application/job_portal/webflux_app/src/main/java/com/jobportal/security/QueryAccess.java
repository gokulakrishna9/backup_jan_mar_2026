package com.jobportal.security;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Declares which custom query a controller method executes.
 * Used by AuthorizationAspect to check queryGroupMemberships JWT claim.
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface QueryAccess {
    String queryName();
}