

package server.repository;

import javax.persistence.*;
import java.util.List;
import java.util.Optional;

@Entity
@Table(name = "program_registrations")
public class ProgramRegistration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long registrationId;

    @Column(name = "program_id")
    private Long programId;

    @Column(name = "patron_id")
    private Long patronId;

    @Column(name = "attendance_log")
    private String attendanceLog;

    @Column(name = "payment_status")
    private String paymentStatus;

    public Long getRegistrationId() {
        return registrationId;
    }

    public void setRegistrationId(Long registrationId) {
        this.registrationId = registrationId;
    }

    public Long getProgramId() {
        return programId;
    }

    public void setProgramId(Long programId) {
        this.programId = programId;
    }

    public Long getPatronId() {
        return patronId;
    }

    public void setPatronId(Long patronId) {
        this.patronId = patronId;
    }

    public String getAttendanceLog() {
        return attendanceLog;
    }

    public void setAttendanceLog(String attendanceLog) {
        this.attendanceLog = attendanceLog;
    }

    public String getPaymentStatus() {
        return paymentStatus;
    }

    public void setPaymentStatus(String paymentStatus) {
        this.paymentStatus = paymentStatus;
    }

    public boolean isValid() {
        return registrationId != null && programId != null && patronId != null;
    }
}

public class ProgramRegistrationRepository {

    @PersistenceContext
    private EntityManager entityManager;

    public ProgramRegistration getRegistrationData(Long registrationId) {
        return entityManager.find(ProgramRegistration.class, registrationId);
    }
}

public class ProgramRegistrationService {

    @Autowired
    private ProgramRegistrationRepository programRegistrationRepository;

    public ProgramRegistrationStatus getRegistrationStatus(Long registrationId) {
        ProgramRegistration registrationData = programRegistrationRepository.getRegistrationData(registrationId);
        if (registrationData == null || !registrationData.isValid()) {
            return new ProgramRegistrationStatus("Invalid registration data");
        }
        return new ProgramRegistrationStatus(registrationData.getRegistrationId(), registrationData.getProgramId(), registrationData.getPatronId(), registrationData.getAttendanceLog(), registrationData.getPaymentStatus());
    }
}

public class ProgramRegistrationStatus {

    private String error;
    private Long registrationId;
    private Long programId;
    private Long patronId;
    private String attendanceLog;
    private String paymentStatus;

    public ProgramRegistrationStatus(String error) {
        this.error = error;
    }

    public ProgramRegistrationStatus(Long registrationId, Long programId, Long patronId, String attendanceLog, String paymentStatus) {
        this.registrationId = registrationId;
        this.programId = programId;
        this.patronId = patronId;
        this.attendanceLog = attendanceLog;
        this.paymentStatus = paymentStatus;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public Long getRegistrationId() {
        return registrationId;
    }

    public void setRegistrationId(Long registrationId) {
        this.registrationId = registrationId;
    }

    public Long getProgramId() {
        return programId;
    }

    public void setProgramId(Long programId) {
        this.programId = programId;
    }

    public Long getPatronId() {
        return patronId;
    }

    public void setPatronId(Long patronId) {
        this.patronId = patronId;
    }

    public String getAttendanceLog() {
        return attendanceLog;
    }

    public void setAttendanceLog(String attendanceLog) {
        this.attendanceLog = attendanceLog;
    }

    public String getPaymentStatus() {
        return paymentStatus;
    }

    public void setPaymentStatus(String paymentStatus) {
        this.paymentStatus = paymentStatus;
    }
}