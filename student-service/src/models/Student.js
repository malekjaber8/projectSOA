const mongoose = require('mongoose');

const studentSchema = new mongoose.Schema({
  matricule: { 
    type: String, 
    required: true, 
    unique: true 
  },
  nom: { 
    type: String, 
    required: true 
  },
  prenom: { 
    type: String, 
    required: true 
  },
  email: { 
    type: String, 
    required: true, 
    unique: true,
    lowercase: true 
  },
  niveau: { 
    type: String, 
    required: true,
    enum: ['L1', 'L2', 'L3', 'M1', 'M2'] 
  },
  specialite: { 
    type: String, 
    required: true
     
  },
  dateNaissance: { 
    type: Date, 
    required: true 
  },
  dateInscription: { 
    type: Date, 
    default: Date.now 
  }
}, {
  timestamps: true 
});

module.exports = mongoose.model('Student', studentSchema);