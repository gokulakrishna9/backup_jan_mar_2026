package com.example.security;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Declares the required CRUD operation for a controller method.
 * Used by AuthorizationWebFilter to check the tableAccess JWT claim.
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface TableAccess {
    String operation();
}