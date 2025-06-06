from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.api import deps
from app.models.user import UserCreate, Token, UserResponse
from app.services.auth import AuthService
from app.db.models import User  # 从正确的模块导入

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(
    user_in: UserCreate,
    db: Session = Depends(deps.get_db)
) -> Token:
    """用户注册
    
    Args:
        user_in: 用户注册信息
        db: 数据库会话
        
    Returns:
        Token: 访问令牌
        
    Raises:
        HTTPException: 邮箱已被注册时抛出
    """
    try:
        logger.info(f"开始注册用户: {user_in.email}")
        auth_service = AuthService(db)
        
        # 检查邮箱是否已被注册
        if auth_service.get_user_by_email(user_in.email):
            logger.warning(f"邮箱已被注册: {user_in.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被注册"
            )
            
        # 检查用户名是否已被使用
        existing_user = db.query(User).filter(User.username == user_in.username).first()
        if existing_user:
            logger.warning(f"用户名已被使用: {user_in.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该用户名已被使用"
            )
        
        # 创建新用户
        logger.info(f"创建新用户: {user_in.email}")
        user = auth_service.create_user(user_in)
        
        # 创建访问令牌
        logger.info(f"为用户创建访问令牌: {user.id}")
        token = auth_service.create_token(user.id)
        
        logger.info(f"用户注册成功: {user.email}")
        return token
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"注册失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(deps.get_db)
) -> Token:
    """用户登录
    
    Args:
        form_data: 登录表单数据
        db: 数据库会话
        
    Returns:
        Token: 访问令牌
        
    Raises:
        HTTPException: 邮箱或密码错误时抛出
    """
    try:
        auth_service = AuthService(db)
        
        # 验证用户
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )
        
        # 检查用户状态
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户已被禁用"
            )
        
        # 创建访问令牌
        token = auth_service.create_token(user.id)
        
        return token
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"登录失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: int = Depends(deps.get_current_user_id),
    db: Session = Depends(deps.get_db)
) -> UserResponse:
    """获取当前用户信息
    
    Args:
        current_user_id: 当前用户ID
        db: 数据库会话
        
    Returns:
        UserResponse: 用户信息
        
    Raises:
        HTTPException: 用户不存在时抛出
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(current_user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户信息失败: {str(e)}"
        ) 