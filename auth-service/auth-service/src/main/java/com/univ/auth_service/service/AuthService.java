package com.univ.auth_service.service;

import com.univ.auth_service.config.JwtUtil;
import com.univ.auth_service.dto.*;
import com.univ.auth_service.model.*;
import com.univ.auth_service.repo.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import com.univ.auth_service.dto.ValidateResponse;


@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository repo;
    private final PasswordEncoder encoder;
    private final JwtUtil jwt;

    public void register(RegisterRequest req) {
        if (repo.existsByEmail(req.getEmail()))
            throw new RuntimeException("Email already used");

        Role role = (req.getRole() == null) ? Role.ETUDIANT : req.getRole();

        User user = User.builder()
                .email(req.getEmail())
                .passwordHash(encoder.encode(req.getPassword()))
                .role(role)
                .build();

        repo.save(user);
    }

    public AuthResponse login(LoginRequest req) {
        User user = repo.findByEmail(req.getEmail())
                .orElseThrow(() -> new RuntimeException("Invalid credentials"));

        if (!encoder.matches(req.getPassword(), user.getPasswordHash()))
            throw new RuntimeException("Invalid credentials");

        String token = jwt.generateToken(user.getEmail(), user.getRole());
        return new AuthResponse(token, user.getEmail(), user.getRole());
    }
    public ValidateResponse validateToken(String token) {
    try {
        var claims = jwt.getClaims(token);
        String email = claims.getSubject();
        String roleStr = (String) claims.get("role");

        return new ValidateResponse(true, email, Role.valueOf(roleStr));
    } catch (Exception e) {
        return new ValidateResponse(false, null, null);
    }
}

}
