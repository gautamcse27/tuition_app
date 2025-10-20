"""New migration after stamp

Revision ID: 9ff3d4976ba7
Revises: 8288083d59e7
Create Date: 2025-09-29 20:59:11.035009

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9ff3d4976ba7'
down_revision = '8288083d59e7'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'admin',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    with op.batch_alter_table('student_registration', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('mobile_no',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=256),
               existing_nullable=False)
        # If 'created_at' does NOT exist in production, leave this commented:
        # batch_op.drop_column('created_at')

    with op.batch_alter_table('tuition_requirement', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=400),
               type_=sa.String(length=300),
               existing_nullable=True)
        batch_op.drop_constraint(batch_op.f('tuition_requirement_student_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'student_registration', ['student_id'], ['id'])
        # If 'pdf_filename' does NOT exist in production, leave this commented:
        # batch_op.drop_column('pdf_filename')

    with op.batch_alter_table('tutor_profile', schema=None) as batch_op:
        batch_op.alter_column('subjects',
               existing_type=postgresql.ARRAY(sa.TEXT()),
               type_=sa.ARRAY(sa.String()),
               existing_nullable=False)

    with op.batch_alter_table('tutor_registration', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('mobile_no',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=256),
               existing_nullable=False)
        # If 'created_at' does NOT exist in production, leave this commented:
        # batch_op.drop_column('created_at')

def downgrade():
    op.drop_table('admin')

    with op.batch_alter_table('tutor_registration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True))
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('mobile_no',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    with op.batch_alter_table('tutor_profile', schema=None) as batch_op:
        batch_op.alter_column('subjects',
               existing_type=sa.ARRAY(sa.String()),
               type_=postgresql.ARRAY(sa.TEXT()),
               existing_nullable=False)

    with op.batch_alter_table('tuition_requirement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pdf_filename', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('tuition_requirement_student_id_fkey'), 'student_registration', ['student_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('description',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=400),
               existing_nullable=True)

    with op.batch_alter_table('student_registration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True))
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('mobile_no',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
