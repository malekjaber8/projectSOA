package com.univ.auth_service.dto;

import com.univ.auth_service.model.Role;
import lombok.*;

@Getter @Setter @AllArgsConstructor
public class AuthResponse {
    private String token;
    private String email;
    private Role role;
}
