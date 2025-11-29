package com.univ.auth_service.dto;

import com.univ.auth_service.model.Role;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class ValidateResponse {
    private boolean valid;
    private String email;
    private Role role;
}
