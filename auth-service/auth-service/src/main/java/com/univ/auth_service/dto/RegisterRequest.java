package com.univ.auth_service.dto;

import com.univ.auth_service.model.Role;
import lombok.Getter; import lombok.Setter;

@Getter @Setter
public class RegisterRequest {
    private String email;
    private String password;
    private Role role;
}
