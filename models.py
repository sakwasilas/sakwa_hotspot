from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from connections import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    payments = relationship("Payment", back_populates="package")
    sessions = relationship("HotspotSession", back_populates="package")


class ClientDevice(Base):
    __tablename__ = "client_devices"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=True)
    mac_address = Column(String(50), nullable=False, unique=True)
    ip_address = Column(String(50), nullable=True)
    device_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)

    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    mac_address = Column(String(50), nullable=True)

    merchant_request_id = Column(String(100), nullable=True)
    checkout_request_id = Column(String(100), nullable=True)
    mpesa_receipt_number = Column(String(100), nullable=True)
    transaction_date = Column(String(50), nullable=True)

    status = Column(String(50), default="pending")
    result_code = Column(String(20), nullable=True)
    result_desc = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    package = relationship("Package", back_populates="payments")
    session = relationship("HotspotSession", back_populates="payment", uselist=False)


class HotspotSession(Base):
    __tablename__ = "hotspot_sessions"

    id = Column(Integer, primary_key=True, index=True)

    phone_number = Column(String(20), nullable=False)
    mac_address = Column(String(50), nullable=False)

    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    status = Column(String(50), default="active")
    mikrotik_username = Column(String(100), nullable=True)
    mikrotik_password = Column(String(100), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    package = relationship("Package", back_populates="sessions")
    payment = relationship("Payment", back_populates="session")