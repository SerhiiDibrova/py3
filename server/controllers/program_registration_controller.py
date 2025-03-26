

package server.controllers;

import server.repositories.ProgramRegistrationRepository;
import server.models.RegistrationData;
import server.exceptions.InvalidRegistrationIdException;

public class ProgramRegistrationController {
    private ProgramRegistrationRepository programRegistrationRepository;

    public ProgramRegistrationController(ProgramRegistrationRepository programRegistrationRepository) {
        this.programRegistrationRepository = programRegistrationRepository;
    }

    public Object getRegistrationStatus(String registrationId) {
        RegistrationData registrationData = programRegistrationRepository.getRegistrationData(registrationId);
        if (registrationData == null || !registrationData.isValid()) {
            throw new InvalidRegistrationIdException("Invalid registration ID");
        }
        return new RegistrationStatus(registrationData);
    }

    private class RegistrationStatus {
        private String registrationId;
        private String programId;
        private String patronId;
        private String attendanceLog;
        private String paymentStatus;

        public RegistrationStatus(RegistrationData registrationData) {
            this.registrationId = registrationData.getRegistrationId();
            this.programId = registrationData.getProgramId();
            this.patronId = registrationData.getPatronId();
            this.attendanceLog = registrationData.getAttendanceLog();
            this.paymentStatus = registrationData.getPaymentStatus();
        }

        public String getRegistrationId() {
            return registrationId;
        }

        public String getProgramId() {
            return programId;
        }

        public String getPatronId() {
            return patronId;
        }

        public String getAttendanceLog() {
            return attendanceLog;
        }

        public String getPaymentStatus() {
            return paymentStatus;
        }
    }
}