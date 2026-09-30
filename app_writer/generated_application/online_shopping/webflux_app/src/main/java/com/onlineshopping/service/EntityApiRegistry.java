package com.onlineshopping.service;

import org.springframework.stereotype.Component;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Registry mapping database table names to their REST API base paths.
 * Auto-generated from controller layer definitions.
 */
@Component
public class EntityApiRegistry {

    private static final Map<String, String> TABLE_TO_PATH;

    static {
        Map<String, String> map = new LinkedHashMap<>();

        map.put("user", "/api/users");

        map.put("category", "/api/categorys");

        map.put("product", "/api/products");

        map.put("cart", "/api/carts");

        map.put("cart_item", "/api/cart_items");

        map.put("address", "/api/addresss");

        map.put("order", "/api/orders");

        map.put("order_item", "/api/order_items");

        map.put("payment", "/api/payments");

        map.put("review", "/api/reviews");

        TABLE_TO_PATH = Collections.unmodifiableMap(map);
    }

    /**
     * Get the API base path for a table name.
     * @return base path or null if table has no API
     */
    public String getBasePath(String tableName) {
        return TABLE_TO_PATH.get(tableName);
    }

    /**
     * Get all table-to-path mappings.
     */
    public Map<String, String> getAllMappings() {
        return TABLE_TO_PATH;
    }
}