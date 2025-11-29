package com.univ.auth_service.controller;

import com.univ.auth_service.dto.*;
import com.univ.auth_service.service.AuthService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.univ.auth_service.dto.ValidateResponse;


@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService service;

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegisterRequest req) {
        service.register(req);
        return ResponseEntity.ok("registered");
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest req) {
        return ResponseEntity.ok(service.login(req));
    }
    

    @GetMapping("/ping")
    public String ping() { return "auth ok"; }
    @GetMapping("/validate")
public ValidateResponse validate(@RequestHeader("Authorization") String authHeader) {
    String token = authHeader.replace("Bearer ", "").trim();
    return service.validateToken(token);
}

}
