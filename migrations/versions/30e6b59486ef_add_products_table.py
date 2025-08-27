from alembic import op
import sqlalchemy as sa

revision = "add_products_20250827"
down_revision = "ace3bcce6db8"  # <- your last revision id
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("category", sa.String(120)),
        sa.Column("image", sa.String(400)),
        sa.Column("rating_rate", sa.Float, server_default="0"),
        sa.Column("rating_count", sa.Integer, server_default="0"),
        sa.Column("description", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

def downgrade():
    op.drop_table("products")
