from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '<put your new rev id here>'
down_revision = '<previous rev id here>'  # keep whatever was generated
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('image', sa.String(length=500), nullable=True),
        sa.Column('rating_rate', sa.Float(), nullable=False, server_default='0'),
        sa.Column('rating_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )
    # optional: index for sorting by newest
    op.create_index('ix_products_created_at', 'products', ['created_at'])

def downgrade():
    op.drop_index('ix_products_created_at', table_name='products')
    op.drop_table('products')
