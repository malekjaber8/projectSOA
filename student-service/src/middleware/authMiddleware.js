const jwt = require('jsonwebtoken');

const authMiddleware = (req, res, next) => {
  // Récupérer le token du header
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ 
      error: 'Accès refusé. Token JWT requis.' 
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    // Vérifier le token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Ajouter les infos utilisateur à la requête
    req.user = decoded;
    
    next(); // Continuer vers la route
  } catch (error) {
    return res.status(403).json({ 
      error: 'Token JWT invalide ou expiré.' 
    });
  }
};

module.exports = authMiddleware;